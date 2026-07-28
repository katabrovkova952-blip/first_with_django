import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from books.models import Book


@pytest.fixture
def make_user():
    def _make_user(username="user", password="pass12345", is_staff=False):
        return User.objects.create_user(username=username, password=password, is_staff=is_staff)
    return _make_user


@pytest.fixture
def user():
    return User.objects.create_user(username="kateryna", password="pass12345")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def make_auth_client():
    def _make_auth_client(user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client
    return _make_auth_client



@pytest.fixture
def book():
    return Book.objects.create(title="Книга Каті", author="A", year=2020, total_pages=300)