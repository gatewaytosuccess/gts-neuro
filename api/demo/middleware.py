"""Refuses the actions the nightly reset can't undo, or that would break the demo for
the next visitor. Everything else stays usable and is reset each night.

Off unless a demo account email is set, so other environments and tests are unaffected.
"""

from django.conf import settings
from django.http import JsonResponse

from enrollments.models import Enrollment

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

BLOCKED = {
    "admin-user-detail",  # role changes
    "admin-user-suspend",
    "admin-user-reinstate",
    "admin-order-refund",
    "admin-course-thumbnail-upload",
    "admin-lesson-uploads",
    "admin-course-unpublish",
    "checkout",
}


def demo_emails():
    return [email for email in (settings.DEMO_LEARNER_EMAIL, settings.DEMO_ADMIN_EMAIL) if email]


def disabled():
    return JsonResponse({"detail": "Disabled in the demo.", "code": "demo_disabled"}, status=403)


class DemoGuardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method in SAFE_METHODS or not demo_emails():
            return None
        name = request.resolver_match.url_name
        if name in BLOCKED:
            return disabled()
        if name == "admin-enrollment-revoke" and self.is_demo_enrollment(view_kwargs["pk"]):
            return disabled()
        return None

    def is_demo_enrollment(self, pk):
        owner = Enrollment.objects.filter(pk=pk).values_list("user__email", flat=True).first()
        return owner is not None and owner.lower() in {email.lower() for email in demo_emails()}
