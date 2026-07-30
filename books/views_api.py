from typing import Any

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS, AllowAny, BasePermission
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from .models import Book, Review, Shelf
from .serializers import BookSerializer, RegisterSerializer, ReviewSerializer, ShelfSerializer


class IsOwner(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: APIView, obj:Any) -> bool:
        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in SAFE_METHODS or request.user.is_staff


class ShelfViewSet(viewsets.ModelViewSet):
    serializer_class = ShelfSerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> QuerySet[Shelf]:
        assert isinstance(self.request.user, User)
        return Shelf.objects.filter(user=self.request.user)

    def perform_create(self, serializer: BaseSerializer[Shelf]) -> None:
        serializer.save(user=self.request.user)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'year']
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['year', 'created_at', 'title']

    def get_queryset(self) -> QuerySet[Book]:
        return Book.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner]

    def get_queryset(self) -> QuerySet[Review]:
        assert isinstance(self.request.user, User)
        return Review.objects.filter(shelf__user=self.request.user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
