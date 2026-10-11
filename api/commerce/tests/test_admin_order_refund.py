import uuid

import pytest
from django.urls import reverse
from django.utils import timezone

from commerce.checkout import record_refund
from commerce.models import Order, OrderItem, OrderStatus
from enrollments.models import Enrollment, EnrollmentSource, EnrollmentStatus
from users.authentication import ClerkAuthentication
from users.models import Role, User

from .helpers import make_course, refunded_charge

pytestmark = pytest.mark.django_db


@pytest.fixture
def signed_in(monkeypatch):
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


@pytest.fixture
def course():
    return make_course()


def make_order(user, course, status=OrderStatus.PAID, **fields):
    fields.setdefault("payment_intent_id", "pi_test")
    order = Order.objects.create(
        user=user,
        status=status,
        subtotal_cents=course.price_cents,
        total_cents=course.price_cents,
        **fields,
    )
    OrderItem.objects.create(order=order, course=course, unit_price_cents=course.price_cents)
    return order


@pytest.fixture
def order(buyer, course):
    order = make_order(buyer, course)
    Enrollment.objects.create(
        user=buyer, course=course, source=EnrollmentSource.PURCHASE, order=order
    )
    return order


def refund(client, order_id, body=None):
    return client.post(
        reverse("admin-order-refund", args=[order_id]),
        {"reason": "Bought by mistake."} if body is None else body,
        content_type="application/json",
        headers={"Authorization": "Bearer stub"},
    )


class TestAccess:
    def test_rejects_a_request_with_no_token(self, client, order):
        response = client.post(reverse("admin-order-refund", args=[order.pk]))
        assert response.status_code == 401

    @pytest.mark.parametrize("role", [Role.LEARNER, Role.INSTRUCTOR])
    def test_forbids_every_other_role(self, client, signed_in, fake_stripe, order, role):
        User.objects.create_user(email="admin@example.com", clerk_user_id="user_admin", role=role)

        assert refund(client, order.pk).status_code == 403
        assert fake_stripe.calls == []

    def test_an_unknown_order_is_a_404(self, client, admin, fake_stripe):
        assert refund(client, uuid.uuid4()).status_code == 404


class TestRefund:
    def test_marks_the_order_refunded_by_the_admin(self, client, admin, fake_stripe, order):
        before = timezone.now()

        response = refund(client, order.pk)

        assert response.status_code == 200, response.json()
        order.refresh_from_db()
        assert order.status == OrderStatus.REFUNDED
        assert order.refunded_cents == order.total_cents
        assert order.refunded_at >= before
        assert order.refunded_by == admin
        assert order.refund_reason == "Bought by mistake."

    def test_answers_with_the_detail_payload(self, client, admin, fake_stripe, order):
        body = refund(client, order.pk).json()

        assert body["id"] == str(order.pk)
        assert body["status"] == OrderStatus.REFUNDED
        assert body["refunded_by"] == {"id": str(admin.pk), "name": "Grace"}
        assert body["refund_reason"] == "Bought by mistake."
        assert [e["status"] for e in body["enrollments"]] == [EnrollmentStatus.ACTIVE]

    def test_refunds_the_total_through_stripe(self, client, admin, fake_stripe, order):
        refund(client, order.pk)

        assert fake_stripe.named("create_refund") == [
            (
                "create_refund",
                ("pi_test",),
                {
                    "amount": order.total_cents,
                    "reason": "requested_by_customer",
                    "metadata": {"admin_user_id": str(admin.pk)},
                    "idempotency_key": f"admin-refund-{order.pk}-{order.total_cents}",
                },
            )
        ]

    def test_refunds_only_the_remainder_after_a_partial_refund(
        self, client, admin, fake_stripe, order
    ):
        order.refunded_cents = 500
        order.save()

        refund(client, order.pk)

        [(_, _, kwargs)] = fake_stripe.named("create_refund")
        assert kwargs["amount"] == order.total_cents - 500
        order.refresh_from_db()
        assert order.status == OrderStatus.REFUNDED
        assert order.refunded_cents == order.total_cents

    def test_keeps_the_enrollments_active(self, client, admin, fake_stripe, order):
        refund(client, order.pk)

        assert list(order.enrollments.values_list("status", "revoked_at")) == [
            (EnrollmentStatus.ACTIVE, None)
        ]

    def test_an_admin_can_refund_their_own_order(self, client, admin, fake_stripe, course):
        own = make_order(admin, course)

        assert refund(client, own.pk).status_code == 200
        own.refresh_from_db()
        assert (own.status, own.refunded_by) == (OrderStatus.REFUNDED, admin)

    def test_the_webhook_that_follows_changes_nothing(self, client, admin, fake_stripe, order):
        refund(client, order.pk)
        before = Order.objects.values().get(pk=order.pk)

        record_refund(order, refunded_charge(amount_refunded=order.total_cents))

        assert Order.objects.values().get(pk=order.pk) == before


class TestRefusals:
    @pytest.mark.parametrize(
        "body", [{}, {"reason": ""}, {"reason": "   "}], ids=["missing", "empty", "blank"]
    )
    def test_a_missing_or_blank_reason_is_a_400(self, client, admin, fake_stripe, order, body):
        response = refund(client, order.pk, body)

        assert response.status_code == 400
        assert response.json()["reason"] == ["Give a reason for refunding this order."]
        assert fake_stripe.calls == []

    def test_a_reason_over_500_characters_is_a_400(self, client, admin, fake_stripe, order):
        response = refund(client, order.pk, {"reason": "x" * 501})

        assert response.status_code == 400
        assert "reason" in response.json()

    @pytest.mark.parametrize(
        "status", [OrderStatus.PENDING, OrderStatus.REFUNDED, OrderStatus.EXPIRED]
    )
    def test_an_order_that_isnt_paid_is_a_409(
        self, client, admin, fake_stripe, buyer, course, status
    ):
        other = make_order(buyer, course, status=status)

        response = refund(client, other.pk)

        assert response.status_code == 409
        assert fake_stripe.calls == []
        other.refresh_from_db()
        assert other.status == status

    def test_an_order_with_no_payment_intent_is_a_409(
        self, client, admin, fake_stripe, buyer, course
    ):
        legacy = make_order(buyer, course, payment_intent_id="")

        response = refund(client, legacy.pk)

        assert response.status_code == 409
        assert "Stripe dashboard" in response.json()["detail"]
        assert fake_stripe.calls == []

    def test_a_refund_stripe_refuses_is_a_502_and_writes_nothing(
        self, client, admin, fake_stripe, order
    ):
        fake_stripe.refuse_refunds = True
        before = Order.objects.values().get(pk=order.pk)

        response = refund(client, order.pk)

        assert response.status_code == 502
        assert response.json() == {"detail": "Charge ch_test has been disputed."}
        assert Order.objects.values().get(pk=order.pk) == before
