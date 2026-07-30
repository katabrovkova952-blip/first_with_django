import pytest

from books.models import Book, Review, Shelf


@pytest.mark.django_db
def test_books_list_accessible_to_everyone(api_client, auth_client):
    response_anon = api_client.get('/api/books/')
    assert response_anon.status_code == 200

    response_auth = auth_client.get('/api/books/')
    assert response_auth.status_code == 200


@pytest.mark.django_db
def test_create_book_forbidden_for_regular_user(auth_client):
    data = {'title': 'Зіпсований', 'author': 'Пенелопа Дуглас', 'year': 2021, 'total_pages': 300}
    response = auth_client.post('/api/books/', data, format='json')

    assert response.status_code == 403
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_create_book_allowed_for_staff(make_user, make_auth_client):
    admin = make_user(username='admin', is_staff=True)
    admin_client = make_auth_client(admin)

    data = {'title': 'Зіпсований', 'author': 'Пенелопа Дуглас', 'year': 2021, 'total_pages': 300}
    response = admin_client.post('/api/books/', data, format='json')

    assert response.status_code == 201
    assert Book.objects.count() == 1


@pytest.mark.django_db
def test_update_book_forbidden_for_regular_user(auth_client, book):
    response = auth_client.patch(f'/api/books/{book.id}/', {'title': 'Зіпсований'}, format='json')

    assert response.status_code == 403
    assert Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_update_book_allowed_for_staff(make_user, make_auth_client, book):
    admin = make_user(username='admin', is_staff=True)
    admin_client = make_auth_client(admin)

    response = admin_client.patch(f'/api/books/{book.id}/', {'title': 'Оновлена назва'}, format='json')

    assert response.status_code == 200
    book.refresh_from_db()
    assert book.title == 'Оновлена назва'


@pytest.mark.django_db
def test_delete_book_forbidden_for_regular_user(auth_client, book):
    response = auth_client.delete(f'/api/books/{book.id}/', format='json')

    assert response.status_code == 403
    assert Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_delete_book_allowed_for_staff(make_user, make_auth_client, book):
    admin = make_user(username='admin', is_staff=True)
    admin_client = make_auth_client(admin)

    response = admin_client.delete(f'/api/books/{book.id}/', format='json')

    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_delete_book_in_shelf(auth_client, user, book):
    shelf = Shelf.objects.create(user=user, book=book)
    response = auth_client.delete(f'/api/shelf/{shelf.pk}/')

    assert response.status_code == 204
    assert not Shelf.objects.filter(id=shelf.pk).exists()
    assert Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_added_book_in_shelf(auth_client, user, book):
    response = auth_client.post('/api/shelf/', {'book': book.id}, format='json')

    assert response.status_code == 201
    assert Shelf.objects.count() == 1


@pytest.mark.django_db
def test_shelf_confidentiality(auth_client, user, make_user, make_auth_client, book):
    stranger = make_user(username='stranger')
    stranger_client = make_auth_client(stranger)

    owner_shelf = Shelf.objects.create(user=user, book=book)

    response = stranger_client.get(f'/api/shelf/{owner_shelf.pk}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_review_confidentiality(auth_client, user, make_user, make_auth_client, book):
    stranger = make_user(username='stranger')
    stranger_client = make_auth_client(stranger)

    owner_shelf = Shelf.objects.create(user=user, book=book, status='finished')
    review = Review.objects.create(shelf=owner_shelf, rating=5, text='Супер')

    response = stranger_client.get(f'/api/review/{review.pk}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_can_not_write_review_before_finished(auth_client, user, book):
    shelf = Shelf.objects.create(user=user, book=book, status='reading')
    response = auth_client.post(
        '/api/review/',
        {'shelf': shelf.pk, 'rating': 5, 'text': 'Супер'},
        format='json',
    )

    assert response.status_code == 400
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_can_write_review_after_finished(auth_client, user, book):
    shelf = Shelf.objects.create(user=user, book=book, status='finished')
    response = auth_client.post(
        '/api/review/',
        {'shelf': shelf.pk, 'rating': 5, 'text': 'Супер'},
        format='json',
    )

    assert response.status_code == 201
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_can_not_write_review_for_strange_recording(make_user, make_auth_client, user, book):
    shelf = Shelf.objects.create(user=user, book=book, status='finished')
    stranger = make_user(username='stranger')
    stranger_client = make_auth_client(stranger)

    response = stranger_client.post(
        '/api/review/',
        {'shelf': shelf.pk, 'rating': 5, 'text': 'Супер'},
        format='json',
    )

    assert response.status_code == 400
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_current_page_is_persisted(auth_client, user, book):
    shelf = Shelf.objects.create(user=user, book=book)

    patch_response = auth_client.patch(
        f'/api/shelf/{shelf.pk}/',
        {'current_page': 35},
        format='json',
    )
    assert patch_response.status_code == 200

    get_response = auth_client.get(f'/api/shelf/{shelf.pk}/')
    assert get_response.status_code == 200
    assert get_response.data['current_page'] == 35


@pytest.mark.django_db
def test_current_page_can_not_be_bigger_than_total_pages(auth_client, user, book):
    shelf = Shelf.objects.create(user=user, book=book)
    patch_response = auth_client.patch(
        f'/api/shelf/{shelf.pk}/',
        {'current_page': 350},
        format='json',
    )

    assert patch_response.status_code == 400
    assert 'current_page' in patch_response.data


@pytest.mark.parametrize(
    'book',
    [
        pytest.param(
            {'title': 'Смерть на нілі', 'author': 'Агата Крісті',
             'year': 1449, 'total_pages': 300}, id='1449 year'
        ),
        pytest.param(
            {'title': 'Витончене мистецтво', 'author': 'Марк Менсон',
             'year': 3001, 'total_pages': 300}, id='3001 year'
        ),
        pytest.param(
            {'title': 'Пошук сенсу', 'author': 'Віктор Франкл',
             'year': -500, 'total_pages': 300}, id='-500 year'
        ),
    ],
)
@pytest.mark.django_db
def test_raises_year(make_auth_client, make_user, book):
    admin = make_user(username='admin', is_staff=True)
    admin_client = make_auth_client(admin)

    response = admin_client.post('/api/books/', book, format='json')
    assert response.status_code == 400
    assert 'year' in response.data
    assert Book.objects.count() == 0
