from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('add/', views.add_book, name='add_book'),
    path('book/<int:id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:id>/delete/', views.delete_book, name='delete_book'),
]