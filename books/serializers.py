from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'user', 'title', 'author', 'description',
                  'year', 'created_at', 'is_published']
        read_only_fields = ['id', 'user', 'created_at']
