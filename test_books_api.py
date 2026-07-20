import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from books.models import Book


@pytest.mark.django_db
def test_public_list_shows_only_published():
    # ARRANGE — готуємо дані в тестовій базі
    user = User.objects.create_user(username="kateryna", password="pass12345")
    Book.objects.create(user=user, title="Публічна", author="A", year=2020, is_published=True)
    Book.objects.create(user=user, title="Приватна", author="B", year=2021, is_published=False)

    # ACT — робимо запит
    client = APIClient()
    response = client.get("/api/public-books/")

    # ASSERT — перевіряємо відповідь
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Публічна"


@pytest.mark.django_db
def test_books_requires_auth(api_client):
    #Анонім
    response = api_client.get("/api/books/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_books_accessible_when_logged_in(auth_client):
    response = auth_client.get("/api/books/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_idor(auth_client, user, make_user):
    stranger = make_user(username="stranger")
    Book.objects.create(user=user, title="Книга власника", author="A", year=2020)
    Book.objects.create(user=stranger, title="Книга чужого", author="B", year=2021)
    response = auth_client.get("/api/books/")
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == "Книга власника"


@pytest.mark.django_db
def test_create_book(auth_client, user):
    data = {"title": "Зіпсований", "author": "Пенелопа Дуглас", "year": 2021}
    response = auth_client.post("/api/books/", data, format="json")

    assert response.status_code == 201
    assert Book.objects.count() == 1
    assert Book.objects.first().user == user


@pytest.mark.django_db
def test_update_book(auth_client, book):
    data = {"title": "Змінена книга"}
    response = auth_client.patch(f"/api/books/{book.id}/", data, format="json")

    assert response.status_code == 200
    book.refresh_from_db()          # перезавантажуємо з бази
    assert book.title == "Змінена книга"


@pytest.mark.django_db
def test_delete_book(auth_client, book):
    response = auth_client.delete(f"/api/books/{book.id}/")
    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.parametrize("book", [
    pytest.param({"title": "Смерть на нілі", "author": "Агата Крісті", "year": 1449},  id="1449 year"),
    pytest.param({"title": "Витончене мистецтво", "author": "Марк Менсон", "year": 3001}, id="3001 year"),
    pytest.param({"title": "Пошук сенсу", "author": "Віктор Франкл", "year": -500}, id="-500 year")
])
@pytest.mark.django_db
def test_raises_year(book, auth_client):
    response = auth_client.post("/api/books/", book, format="json")
    assert response.status_code == 400
    assert "year" in response.data
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_unique_title(auth_client, user):
    Book.objects.create(user=user, title="Дюна", author="A", year=2020)
    book = {"title": "Дюна", "author": "B", "year": 2021}
    response = auth_client.post("/api/books/", book, format="json")

    assert response.status_code == 400
    assert Book.objects.count() == 1
    assert 'non_field_errors' in response.data


