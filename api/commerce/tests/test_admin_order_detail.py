import uuid

import pytest
from django.urls import reverse
from django.utils import timezone

from commerce.models import Coupon, DiscountType, Order, OrderItem, OrderStatus
from enrollments.models import Enrollment, EnrollmentSource, EnrollmentStatus
from users.authentication import ClerkAuthentication
from users.models import Role, User, UserStatus

from .helpers import make_course

pytestmark = pytest.mark.django_db


@pytest.fixture
def signed_in(monkeypatch):
    """Stubs only token verification; the status check runs for real."""
    monkeypatch.setattr(
        ClerkAuthentication, "decode_token", lambda self, token: {"sub": "user_admin"}
    )


@pytest.fixture
def admin(signed_in):
    return User.objects.create_user(
        email="admin@example.com", name="Grace", clerk_user_id="user_admin", role=Role.ADMIN
    )


@pytest.fixture
def buyer():
    return User.objects.create_user(email="ada@example.com", name="Ada")


def make_order(user, courses=(), status=OrderStatus.PAID, **fields):
    total = sum(course.price_cents for course in courses)
    fields.setdefault("subtotal_cents", total)
    fields.setdefault("total_cents", total)
    order = Order.objects.create(user=user, status=status, **fields)
    for course in courses:
        OrderItem.objects.create(order=order, course=course, unit_price_cents=course.price_cents)
    return order


def enroll(order, course, **fields):
    return Enrollment.objects.create(
        user=order.user, course=course, source=EnrollmentSource.PURCHASE, order=order, **fields
    )


def get_order(client, order_id):
    return client.get(
        reverse("admin-order-detail", args=[order_id]), headers={"Authorization": "Bearer stub"}
    )


def fetch_order(client, order_id):
    response = get_order(client, order_id)
    assert response.status_code == 200, response.json()
    return response.json()


class TestAccess:
    def test_rejects_a_request_with_no_token(self, client, buyer):
        order = make_order(buyer)
        assert client.get(reverse("admin-order-detail", args=[order.pk])).status_code == 401

    @pytest.mark.parametrize("role", [Role.LEARNER, Role.INSTRUCTOR])
    def test_forbids_every_other_role(self, client, signed_in, buyer, role):
        User.objects.create_user(email="admin@example.com", clerk_user_id="user_admin", role=role)
        order = make_order(buyer)
        assert get_order(client, order.pk).status_code == 403

    def test_an_unknown_order_is_a_404(self, client, admin):
        assert get_order(client, uuid.uuid4()).status_code == 404


class TestPaidOrder:
    def test_returns_the_order_with_its_buyer_items_and_coupon(self, client, admin, buyer):
        zeta = make_course("zeta", price_cents=5000)
        alpha = make_course("alpha", price_cents=3000)
        coupon = Coupon.objects.create(
            code="SPRING", discount_type=DiscountType.FIXED, discount_value=1000
        )
        order = make_order(
            buyer,
            [zeta, alpha],
            coupon=coupon,
            subtotal_cents=8000,
            discount_cents=1000,
            total_cents=7000,
            payment_intent_id="pi_123",
            receipt_url="https://pay.stripe.com/receipts/123",
        )

        body = fetch_order(client, order.pk)

        assert body["id"] == str(order.pk)
        assert body["status"] == "paid"
        assert body["created_at"] and body["updated_at"]
        assert body["subtotal_cents"] == 8000
        assert body["coupon_code"] == "SPRING"
        assert body["discount_cents"] == 1000
        assert body["total_cents"] == 7000
        assert body["receipt_url"] == "https://pay.stripe.com/receipts/123"
        assert body["buyer"] == {
            "id": str(buyer.pk),
            "name": "Ada",
            "email": "ada@example.com",
            "status": "active",
        }
        assert body["items"] == [
            {"course_id": str(alpha.pk), "title": "Alpha", "unit_price_cents": 3000},
            {"course_id": str(zeta.pk), "title": "Zeta", "unit_price_cents": 5000},
        ]

    def test_without_a_coupon_or_refund_those_fields_are_blank(self, client, admin, buyer):
        order = make_order(buyer, [make_course()])

        body = fetch_order(client, order.pk)

        assert body["coupon_code"] is None
        assert body["discount_cents"] == 0
        assert body["refunded_cents"] == 0
        assert body["refunded_at"] is None
        assert body["refunded_by"] is None
        assert body["refund_reason"] == ""

    def test_shows_a_partial_refund_made_in_stripe(self, client, admin, buyer):
        order = make_order(buyer, [make_course()], refunded_cents=500)

        body = fetch_order(client, order.pk)

        assert body["status"] == "paid"
        assert body["refunded_cents"] == 500
        assert body["refunded_by"] is None

    def test_shows_who_refunded_it_and_why(self, client, admin, buyer):
        refunded_at = timezone.now()
        order = make_order(
            buyer,
            [make_course()],
            status=OrderStatus.REFUNDED,
            refunded_cents=12900,
            refunded_at=refunded_at,
            refunded_by=admin,
            refund_reason="Bought by mistake.",
        )

        body = fetch_order(client, order.pk)

        assert body["status"] == "refunded"
        assert body["refunded_cents"] == 12900
        assert body["refunded_at"] is not None
        assert body["refunded_by"] == {"id": str(admin.pk), "name": "Grace"}
        assert body["refund_reason"] == "Bought by mistake."

    def test_shows_a_suspended_buyer_as_suspended(self, client, admin):
        buyer = User.objects.create_user(email="sus@example.com", status=UserStatus.SUSPENDED)
        order = make_order(buyer, [make_course()])

        assert fetch_order(client, order.pk)["buyer"]["status"] == "suspended"


class TestStripePaymentUrl:
    def test_links_to_the_live_dashboard_under_a_live_key(self, client, admin, buyer, settings):
        settings.STRIPE_SECRET_KEY = "sk_live_abc"
        order = make_order(buyer, [make_course()], payment_intent_id="pi_123")

        assert (
            fetch_order(client, order.pk)["stripe_payment_url"]
            == "https://dashboard.stripe.com/payments/pi_123"
        )

    def test_links_under_test_with_a_test_key(self, client, admin, buyer, settings):
        settings.STRIPE_SECRET_KEY = "sk_test_abc"
        order = make_order(buyer, [make_course()], payment_intent_id="pi_123")

        assert (
            fetch_order(client, order.pk)["stripe_payment_url"]
            == "https://dashboard.stripe.com/test/payments/pi_123"
        )

    @pytest.mark.parametrize("status", [OrderStatus.PENDING, OrderStatus.EXPIRED])
    def test_an_unpaid_order_has_no_payment_or_receipt_link(self, client, admin, buyer, status):
        order = make_order(buyer, [make_course()], status=status)

        body = fetch_order(client, order.pk)

        assert body["status"] == status
        assert body["stripe_payment_url"] == ""
        assert body["receipt_url"] == ""
        assert body["enrollments"] == []


class TestEnrollments:
    def test_lists_the_enrollments_the_order_produced_by_title(self, client, admin, buyer):
        zeta, alpha = make_course("zeta"), make_course("alpha")
        order = make_order(buyer, [zeta, alpha])
        revoked_at = timezone.now()
        revoked = enroll(order, zeta, status=EnrollmentStatus.REVOKED, revoked_at=revoked_at)
        active = enroll(order, alpha)

        body = fetch_order(client, order.pk)

        assert [row["id"] for row in body["enrollments"]] == [str(active.pk), str(revoked.pk)]
        assert body["enrollments"][0] == {
            "id": str(active.pk),
            "course_id": str(alpha.pk),
            "title": "Alpha",
            "status": "active",
            "revoked_at": None,
        }
        assert body["enrollments"][1]["status"] == "revoked"
        assert body["enrollments"][1]["revoked_at"] is not None

    def test_leaves_out_an_enrollment_a_later_order_took_over(self, client, admin, buyer):
        course = make_course()
        first = make_order(buyer, [course])
        second = make_order(buyer, [course])
        enroll(second, course)

        assert fetch_order(client, first.pk)["enrollments"] == []
        assert len(fetch_order(client, second.pk)["enrollments"]) == 1
