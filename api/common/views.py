from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def ping(request):
    """Liveness probe. Never touches the database, so frequent pings don't keep it awake."""
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """Readiness probe. 503 with the error text if the database is unreachable."""
    try:
        connection.ensure_connection()
    except Exception as exc:
        return Response({"status": "error", "database": str(exc)}, status=503)
    return Response({"status": "ok", "database": "ok"})
