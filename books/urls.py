from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import BookViewSet, ShelfViewSet, ReviewViewSet, RegisterView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'shelf', ShelfViewSet, basename='shelf')
router.register(r'review', ReviewViewSet, basename='review')
app_name = 'books'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register')
]