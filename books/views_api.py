
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer, PublicBookSerializer
from rest_framework.permissions import BasePermission


class BookViewSet(viewsets.ModelViewSet):

    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'year', 'is_published']
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['year', 'created_at', 'title']

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)


class PublicBookListView(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PublicBookSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'year']
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['year', 'title']

    def get_queryset(self):
        return Book.objects.filter(is_published=True)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user