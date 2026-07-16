from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer, PublicBookSerializer


class BookViewSet(ListModelMixin, RetrieveModelMixin,
                  UpdateModelMixin, CreateModelMixin, viewsets.GenericViewSet,):

    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicBookListView(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PublicBookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Book.objects.filter(is_published=True)




