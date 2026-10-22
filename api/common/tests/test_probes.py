import pytest
from django.db import connection
from django.db.utils import OperationalError
from django.urls import reverse


def test_ping_is_ok_without_database_access(client):
    # No django_db mark: any query here fails the test.
    response = client.get(reverse("ping"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ping_ignores_a_bad_token(client):
    response = client.get(reverse("ping"), headers={"Authorization": "Bearer junk"})

    assert response.status_code == 200


@pytest.mark.django_db
def test_health_is_ok_when_the_database_is_reachable(client):
    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


@pytest.mark.django_db
def test_health_is_503_when_the_database_is_unreachable(client, monkeypatch):
    def unreachable():
        raise OperationalError("connection refused")

    monkeypatch.setattr(connection, "ensure_connection", unreachable)

    response = client.get(reverse("health"))

    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "connection refused"}
