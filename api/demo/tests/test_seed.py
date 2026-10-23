from io import StringIO

import pytest
from django.core.management import CommandError, call_command
from django.urls import reverse

from commerce.models import Order, OrderStatus
from common.storage import DEMO_PREFIXES
from courses.models import Course, Lesson
from demo import assets, content
from enrollments.models import Enrollment, EnrollmentStatus, LessonProgress
from reviews.models import Review, ReviewStatus
from users.authentication import ClerkAuthentication
from users.models import Role, User

pytestmark = pytest.mark.django_db

LEARNER_EMAIL = "learner@demo.example.com"
ADMIN_EMAIL = "admin@demo.example.com"


@pytest.fixture(autouse=True)
def demo_accounts(settings):
    settings.DEMO_LEARNER_EMAIL = LEARNER_EMAIL
    settings.DEMO_ADMIN_EMAIL = ADMIN_EMAIL


def seed(*args):
    call_command("seed_demo", *args, stdout=StringIO())


# Committed between runs, like the nightly job: one transaction would leave deferred
# constraint checks pending, and Postgres won't TRUNCATE past them.
@pytest.mark.django_db(transaction=True)
def test_reset_runs_twice_cleanly():
    seed("--reset")
    seed("--reset")

    assert Course.objects.count() == len(content.COURSES)
    assert User.objects.count() == len(content.LEARNERS) + 2
    assert Order.objects.count() == len(content.PURCHASES) + len(content.ABANDONED_CHECKOUTS)
    assert Review.objects.count() == len(content.REVIEWS)


@pytest.mark.django_db(transaction=True)
def test_reset_replaces_edits():
    seed("--reset")
    Course.objects.filter(slug="the-bilingual-brain").update(title="Edited")

    seed("--reset")

    assert Course.objects.get(slug="the-bilingual-brain").title == "The Bilingual Brain"


def test_refuses_to_seed_over_existing_courses():
    seed()

    with pytest.raises(CommandError):
        seed()


def test_refuses_without_the_demo_emails(settings):
    settings.DEMO_ADMIN_EMAIL = ""

    with pytest.raises(CommandError):
        seed("--reset")

    assert not Course.objects.exists()


def test_demo_accounts_wait_to_be_linked_by_email():
    seed("--reset")

    learner = User.objects.get(email=LEARNER_EMAIL)
    admin = User.objects.get(email=ADMIN_EMAIL)
    assert (learner.role, admin.role) == (Role.LEARNER, Role.ADMIN)
    assert learner.clerk_user_id is None and admin.clerk_user_id is None


def test_demo_learners_dashboard(client, monkeypatch):
    seed("--reset")
    User.objects.filter(email=LEARNER_EMAIL).update(clerk_user_id="user_demo")
    monkeypatch.setattr(
        ClerkAuthentication, "decode_token", lambda self, token: {"sub": "user_demo"}
    )

    response = client.get(reverse("user-me-enrollments"), headers={"Authorization": "Bearer x"})

    assert response.status_code == 200
    foundations, aphasia = response.json()
    assert foundations["course_slug"] == "foundations-of-neurolinguistics"
    assert (foundations["completed_lesson_count"], foundations["lesson_count"]) == (2, 5)
    assert foundations["continue_lesson_title"] == "How sound reaches the language areas"
    assert aphasia["course_slug"] == "aphasia-and-the-damaged-brain"
    assert aphasia["completed_lesson_count"] == aphasia["lesson_count"] == 5


def test_video_lesson_resumes_partway():
    seed("--reset")

    progress = LessonProgress.objects.get(
        user__email=LEARNER_EMAIL, lesson__video_key=assets.VIDEO.key
    )

    assert 0 < progress.last_position_seconds < assets.VIDEO_DURATION_SECONDS


def test_admin_lists_show_every_kind_of_record():
    seed("--reset")

    statuses = set(Order.objects.values_list("status", flat=True))
    assert statuses == {OrderStatus.PAID, OrderStatus.REFUNDED, OrderStatus.EXPIRED}
    assert Order.objects.get(status=OrderStatus.REFUNDED).refunded_by.email == ADMIN_EMAIL
    assert Enrollment.objects.filter(status=EnrollmentStatus.REVOKED).exists()
    assert Enrollment.objects.filter(order__isnull=True).exists()
    assert Review.objects.filter(status=ReviewStatus.HIDDEN).exists()


def test_every_lesson_has_content_and_media_stays_under_the_demo_prefix():
    seed("--reset")

    for lesson in Lesson.objects.all():
        assert len(lesson.body.split()) >= 100, lesson.title
    keys = [
        *Course.objects.values_list("thumbnail_key", flat=True),
        *Lesson.objects.exclude(video_key="").values_list("video_key", flat=True),
        *Lesson.objects.exclude(slides_key="").values_list("slides_key", flat=True),
    ]
    assert len(keys) == len(assets.ALL)
    assert all(key.startswith(DEMO_PREFIXES) for key in keys)


def test_every_media_file_is_present():
    for asset in assets.ALL:
        assert asset.path.is_file(), asset.filename
