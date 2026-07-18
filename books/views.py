from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.views.generic import DetailView, DeleteView, CreateView, UpdateView, ListView
from django.core.paginator import Paginator

from books.models import Book
from books.forms import BookForm


@login_required
def home(request):
    books = Book.objects.for_user(request.user)

    search = request.GET.get("search", "")

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    paginator = Paginator(books, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home.html",
        {
            "page_obj": page_obj,
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


class BookListView(ListView):
    model = Book
    template_name = 'home.html'
    paginate_by = 3


class BookCreateView(LoginRequiredMixin, CreateView):
    form_class = BookForm
    template_name = 'create.html'
    success_url = reverse_lazy('books:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BookForm
    template_name = 'update.html'
    success_url = reverse_lazy('books:home')

    def get_queryset(self):
        return Book.objects.for_user(self.request.user)


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.for_user(self.request.user)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books:home')

    def get_queryset(self):
        return Book.objects.for_user(self.request.user)


# @login_required
# def book_detail(request, book_id):
#     book = get_object_or_404(
#         Book.objects.for_user(request.user),
#         pk=book_id
#     )
#     return render(request, 'detail.html', {'book': book})

# @login_required
# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.user = request.user
#             book.save()
#             return redirect('home')
#     else:
#         form = BookForm()
#
#     return render(request, 'create.html', {'form': form})


# @login_required
# def edit_book(request, book_id):
#     book = get_object_or_404(
#         Book.objects.for_user(request.user),
#         pk=book_id
#     )
#
#     if request.method == 'POST':
#         form = BookForm(request.POST, instance=book)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = BookForm(instance=book)
#
#     return render(request, 'update.html', {'form': form})


# @login_required
# @require_POST
# def delete_book(request, book_id):
#     book = get_object_or_404(
#         Book.objects.for_user(request.user),
#         pk=book_id
#     )
#     book.delete()
#     return redirect('home')
