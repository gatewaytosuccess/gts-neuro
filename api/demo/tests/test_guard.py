import uuid

import pytest
from django.urls import reverse

from courses.models import Course
from enrollments.models import Enrollment, EnrollmentSource, EnrollmentStatus
from users.authentication import ClerkAuthentication
from users.models import Role, User

pytestmark = pytest.mark.django_db

AUTH = {"Authorization": "Bearer stub"}


@pytest.fixture(autouse=True)
def demo_accounts(settings):
    settings.DEMO_LEARNER_EMAIL = "Learner@demo.example.com"
    settings.DEMO_ADMIN_EMAIL = "admin@demo.example.com"


@pytest.fixture
def admin(monkeypatch):
    user = User.objects.create_user(
        email="admin@demo.example.com", clerk_user_id="user_admin", role=Role.ADMIN
    )
    monkeypatch.setattr(
        ClerkAuthentication, "decode_token", lambda self, token: {"sub": "user_admin"}
    )
    return user


def enrollment_of(email):
    user = User.objects.create_user(email=email)
    course = Course.objects.create(slug=f"c-{uuid.uuid4().hex[:8]}", title="C", price_cents=100)
    return Enrollment.objects.create(user=user, course=course, source=EnrollmentSource.MANUAL)


def assert_disabled(response):
    assert response.status_code == 403
    assert response.json() == {"detail": "Disabled in the demo.", "code": "demo_disabled"}


@pytest.mark.parametrize(
    ("name", "method"),
    [
        ("admin-user-detail", "patch"),
        ("admin-user-suspend", "post"),
        ("admin-user-reinstate", "post"),
        ("admin-order-refund", "post"),
        ("admin-course-thumbnail-upload", "post"),
        ("admin-lesson-uploads", "post"),
        ("admin-course-unpublish", "post"),
    ],
)
def test_blocks_actions_the_reset_cant_undo(client, admin, name, method):
    url = reverse(name, kwargs={"pk": uuid.uuid4()})

    response = getattr(client, method)(url, {}, content_type="application/json", headers=AUTH)

    assert_disabled(response)


def test_blocks_checkout(client, admin):
    response = client.post(
        reverse("checkout"), {"course": "x"}, content_type="application/json", headers=AUTH
    )

    assert_disabled(response)


def test_reading_a_blocked_route_still_works(client, admin):
    response = client.get(reverse("admin-user-detail", kwargs={"pk": admin.pk}), headers=AUTH)

    assert response.status_code == 200


def test_blocks_revoking_a_demo_accounts_enrollment(client, admin):
    enrollment = enrollment_of("learner@demo.example.com")

    response = client.post(
        reverse("admin-enrollment-revoke", kwargs={"pk": enrollment.pk}), headers=AUTH
    )

    assert_disabled(response)
    enrollment.refresh_from_db()
    assert enrollment.status == EnrollmentStatus.ACTIVE


def test_allows_revoking_anyone_elses_enrollment(client, admin):
    enrollment = enrollment_of("priya@example.com")

    response = client.post(
        reverse("admin-enrollment-revoke", kwargs={"pk": enrollment.pk}), headers=AUTH
    )

    assert response.status_code == 200
    enrollment.refresh_from_db()
    assert enrollment.status == EnrollmentStatus.REVOKED


def test_is_off_without_demo_accounts(client, admin, settings):
    settings.DEMO_LEARNER_EMAIL = settings.DEMO_ADMIN_EMAIL = ""

    response = client.post(
        reverse("admin-course-unpublish", kwargs={"pk": uuid.uuid4()}), headers=AUTH
    )

    assert response.status_code == 404
