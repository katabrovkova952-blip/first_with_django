from django.shortcuts import render, redirect, get_object_or_404
from books.models import Book
from books.forms import BookForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

@login_required
def home(request):
    books = Book.objects.for_user(request.user)

    search = request.GET.get("search")

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    return render(
        request,
        "home.html",
        {
            "books": books,
            "search": search,
        },
    )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    books = Book.objects.for_user(request.user)

    return render(request, 'profile.html', {
        'user': request.user,
        'books': books
    })


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(
        Book.objects.for_user(request.user),
        pk=book_id
    )
    return render(request, 'detail.html', {'book': book})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(
        Book.objects.for_user(request.user),
        pk=book_id
    )

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form})

@login_required
@require_POST
def delete_book(request, book_id):
    book = get_object_or_404(
        Book.objects.for_user(request.user),
        pk=book_id
    )
    book.delete()
    return redirect('home')
