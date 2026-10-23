"""Seeds the public demo. Runs with DEBUG off, unlike ``seed_courses``."""

import uuid
from datetime import timedelta

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from commerce.models import Order, OrderItem, OrderStatus
from courses.models import Course, Lesson, Module
from demo import assets, content
from enrollments.models import (
    Enrollment,
    EnrollmentSource,
    EnrollmentStatus,
    LessonProgress,
    ProgressStatus,
)
from reviews.models import Review
from users.models import Role, User


class Command(BaseCommand):
    help = "Fill the demo database with courses, learners, orders and progress."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true", help="Flush every table first, then seed."
        )

    def handle(self, *args, reset=False, **options):
        emails = {
            content.LEARNER: settings.DEMO_LEARNER_EMAIL,
            content.ADMIN: settings.DEMO_ADMIN_EMAIL,
        }
        if not all(emails.values()):
            raise CommandError("Set DEMO_LEARNER_EMAIL and DEMO_ADMIN_EMAIL first.")

        # One transaction, so a seed that fails leaves the flushed data in place.
        with transaction.atomic():
            if reset:
                call_command("flush", interactive=False, verbosity=0)
            elif Course.objects.exists():
                raise CommandError("Courses already exist. Pass --reset to replace everything.")
            Seeder(emails, timezone.now()).run()

        self.stdout.write(self.style.SUCCESS("Seeded the demo."))


class Seeder:
    def __init__(self, emails, now):
        self.emails = emails
        self.now = now
        self.users = {}
        self.courses = {}
        self.lessons = {}
        self.orders = {}
        self.enrollments = {}

    def ago(self, days, hours=0):
        return self.now - timedelta(days=days, hours=hours)

    def run(self):
        self.seed_users()
        for spec in content.COURSES:
            self.seed_course(spec)
        for who, slug, days in content.PURCHASES:
            self.purchase(who, slug, days)
        for who, slug, days, by, reason in content.REFUNDS:
            self.refund(who, slug, days, by, reason)
        for who, slug, source, days in content.GRANTS:
            self.enroll(who, slug, source, self.ago(days))
        for who, slug, days in content.REVOCATIONS:
            self.revoke(who, slug, days)
        for who, slug, days, status in content.ABANDONED_CHECKOUTS:
            self.order(who, slug, status, self.ago(days))
        for who, slug, count, first, last in content.COMPLETIONS:
            self.complete(who, slug, count, first, last)
        for who, slug, title, position, days in content.IN_PROGRESS:
            self.start(who, slug, title, position, days)
        for who, slug, rating, body, status, days in content.REVIEWS:
            self.review(who, slug, rating, body, status, days)

    def seed_users(self):
        people = [
            (content.ADMIN, self.emails[content.ADMIN], content.ADMIN_NAME, Role.ADMIN),
            (content.LEARNER, self.emails[content.LEARNER], content.LEARNER_NAME, Role.LEARNER),
            *((email, email, name, Role.LEARNER) for email, name in content.LEARNERS),
        ]
        for who, email, name, role in people:
            # No clerk_user_id: the first sign-in links the row by email.
            user = User.objects.create_user(email=email, name=name, role=role)
            joined = self.ago(self.first_activity_days(who) + 1)
            User.objects.filter(pk=user.pk).update(created_at=joined, updated_at=joined)
            self.users[who] = user

    def first_activity_days(self, who):
        days = [
            *(days for person, _, days in content.PURCHASES if person == who),
            *(days for person, _, _, days in content.GRANTS if person == who),
            *(days for person, _, days, _ in content.ABANDONED_CHECKOUTS if person == who),
        ]
        return max(days, default=90)

    def seed_course(self, spec):
        created = self.ago(spec["created_days_ago"])
        course = Course.objects.create(
            slug=spec["slug"],
            title=spec["title"],
            description=spec["description"],
            price_cents=spec["price_cents"],
            status=spec["status"],
            thumbnail_key=assets.THUMBNAILS[spec["slug"]].key,
        )
        Course.objects.filter(pk=course.pk).update(created_at=created, updated_at=created)
        lessons = []
        for module_position, (module_title, lesson_specs) in enumerate(spec["modules"], start=1):
            module = Module.objects.create(
                course=course, title=module_title, position=module_position
            )
            for lesson_position, lesson in enumerate(lesson_specs, start=1):
                lessons.append(
                    Lesson.objects.create(
                        module=module,
                        position=lesson_position,
                        title=lesson.title,
                        body=lesson.body,
                        is_preview=lesson.preview,
                        video_key=lesson.video.key if lesson.video else "",
                        slides_key=lesson.slides.key if lesson.slides else "",
                        duration_seconds=lesson.duration_seconds,
                    )
                )
        self.courses[spec["slug"]] = course
        self.lessons[spec["slug"]] = lessons

    def order(self, who, slug, status, at):
        course = self.courses[slug]
        order = Order.objects.create(
            user=self.users[who],
            status=status,
            subtotal_cents=course.price_cents,
            total_cents=course.price_cents,
            payment_ref=f"cs_demo_{uuid.uuid4().hex[:24]}",
        )
        OrderItem.objects.create(order=order, course=course, unit_price_cents=course.price_cents)
        Order.objects.filter(pk=order.pk).update(created_at=at, updated_at=at)
        return order

    def purchase(self, who, slug, days):
        at = self.ago(days)
        order = self.order(who, slug, OrderStatus.PAID, at)
        self.orders[who, slug] = order
        self.enroll(who, slug, EnrollmentSource.PURCHASE, at, order=order)

    def refund(self, who, slug, days, by, reason):
        order = self.orders[who, slug]
        at = self.ago(days)
        Order.objects.filter(pk=order.pk).update(
            status=OrderStatus.REFUNDED,
            refunded_cents=order.total_cents,
            refunded_at=at,
            refunded_by=self.users[by],
            refund_reason=reason,
            updated_at=at,
        )

    def enroll(self, who, slug, source, at, order=None):
        enrollment = Enrollment.objects.create(
            user=self.users[who], course=self.courses[slug], source=source, order=order
        )
        Enrollment.objects.filter(pk=enrollment.pk).update(enrolled_at=at)
        self.enrollments[who, slug] = enrollment

    def revoke(self, who, slug, days):
        Enrollment.objects.filter(pk=self.enrollments[who, slug].pk).update(
            status=EnrollmentStatus.REVOKED, revoked_at=self.ago(days)
        )

    def complete(self, who, slug, count, first, last):
        lessons = self.lessons[slug][:count]
        step = (first - last) / max(count - 1, 1)
        for index, lesson in enumerate(lessons):
            at = self.ago(first - step * index)
            self.progress(
                who,
                lesson,
                ProgressStatus.COMPLETED,
                lesson.duration_seconds or 0,
                at,
                completed_at=at,
            )

    def start(self, who, slug, title, position, days):
        lesson = next(lesson for lesson in self.lessons[slug] if lesson.title == title)
        self.progress(who, lesson, ProgressStatus.IN_PROGRESS, position, self.ago(days))

    def progress(self, who, lesson, status, position, at, completed_at=None):
        row = LessonProgress.objects.create(
            user=self.users[who],
            lesson=lesson,
            status=status,
            last_position_seconds=position,
            completed_at=completed_at,
        )
        LessonProgress.objects.filter(pk=row.pk).update(created_at=at, updated_at=at)

    def review(self, who, slug, rating, body, status, days):
        review = Review.objects.create(
            user=self.users[who], course=self.courses[slug], rating=rating, body=body, status=status
        )
        at = self.ago(days)
        Review.objects.filter(pk=review.pk).update(created_at=at, updated_at=at)
