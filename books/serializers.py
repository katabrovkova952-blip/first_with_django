from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Book
from django.utils import timezone


class BookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Book
        fields = ['id', 'user', 'title', 'author', 'description',
                  'year', 'created_at', 'is_published']
        read_only_fields = ['user', 'created_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=['user', 'title'],
                message="У вас вже є книга з такою назвою.",
            )
        ]

        def validate_year(self, value):
            current_year = timezone.now().year
            if value < 1450 or value > current_year:
                raise serializers.ValidationError("Рік має бути між 1450 і 2026")
            return value







class PublicBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year']