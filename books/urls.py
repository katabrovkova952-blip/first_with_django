from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSetMixin
from . import views
from .views_api import BookViewSet, PublicBookListView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'public-books', PublicBookListView, basename='public-book')
app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('book/create/', views.BookCreateView.as_view(), name='create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete'),

    path('api/', include(router.urls)),
]