from django.conf import settings
from rest_framework import serializers

from enrollments.models import Enrollment
from users.models import User

from .models import Order, OrderItem, OrderStatus


class OrderItemSerializer(serializers.ModelSerializer):
    course_slug = serializers.CharField(source="course.slug", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["course_slug", "course_title", "unit_price_cents"]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "status", "total_cents", "items"]
        read_only_fields = fields


class OrderReceiptSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        fields = [
            *OrderSerializer.Meta.fields,
            "subtotal_cents",
            "discount_cents",
            "receipt_url",
        ]
        read_only_fields = fields


class AdminOrderFiltersSerializer(serializers.Serializer):
    """The order list's ``status`` query parameter; blank means no filter."""

    status = serializers.ChoiceField(choices=OrderStatus.choices, required=False, allow_blank=True)


class AdminOrderBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email"]
        read_only_fields = fields


class AdminOrderListItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["title"]
        read_only_fields = fields


class AdminOrderListSerializer(serializers.ModelSerializer):
    buyer = AdminOrderBuyerSerializer(source="user", read_only=True)
    items = AdminOrderListItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "status", "total_cents", "refunded_cents", "buyer", "items"]
        read_only_fields = fields


class AdminOrderDetailBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "status"]
        read_only_fields = fields


class AdminOrderRefunderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name"]
        read_only_fields = fields


class AdminOrderDetailItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["course_id", "title", "unit_price_cents"]
        read_only_fields = fields


class AdminOrderEnrollmentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "course_id", "title", "status", "revoked_at"]
        read_only_fields = fields


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    """``enrollments`` are the ones the order holds now: one a later order took
    over belongs to that order instead.

    ``stripe_payment_url`` is blank without a ``payment_intent_id``.
    """

    buyer = AdminOrderDetailBuyerSerializer(source="user", read_only=True)
    coupon_code = serializers.CharField(source="coupon.code", read_only=True, allow_null=True)
    refunded_by = AdminOrderRefunderSerializer(read_only=True)
    stripe_payment_url = serializers.SerializerMethodField()
    items = AdminOrderDetailItemSerializer(many=True, read_only=True)
    enrollments = AdminOrderEnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "subtotal_cents",
            "coupon_code",
            "discount_cents",
            "total_cents",
            "refunded_cents",
            "refunded_at",
            "refunded_by",
            "refund_reason",
            "receipt_url",
            "stripe_payment_url",
            "buyer",
            "items",
            "enrollments",
        ]
        read_only_fields = fields

    def get_stripe_payment_url(self, order):
        if not order.payment_intent_id:
            return ""
        # Test-mode objects live under /test/ in the dashboard.
        mode = "test/" if "_test_" in settings.STRIPE_SECRET_KEY else ""
        return f"https://dashboard.stripe.com/{mode}payments/{order.payment_intent_id}"
