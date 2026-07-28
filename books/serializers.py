from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Shelf, Review
from django.utils import timezone


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description',
                  'year', 'created_at', 'total_pages']
        read_only_fields = ['created_at']

    def validate_year(self, value):
        current_year = timezone.now().year
        if value < 1450 or value > current_year:
            raise serializers.ValidationError(f"Рік має бути між 1450 і {current_year}")
        return value


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['id', 'user', 'book', 'current_page', 'status', 'added_at', 'finished_at']
        read_only_fields = ['user', 'added_at', 'finished_at']

    def validate(self, attrs):
        book = attrs.get('book') or (self.instance.book if self.instance else None)
        current_page = attrs.get(
            'current_page',
            self.instance.current_page if self.instance else None,
        )

        if book is not None and current_page is not None:
            if current_page > book.total_pages:
                raise serializers.ValidationError({
                    "current_page": "Поточна сторінка не може бути більшою за кількість сторінок у книзі."
                })
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'shelf', 'text', 'rating', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        shelf = attrs.get('shelf')
        request = self.context['request']

        if shelf.user != request.user:
            raise serializers.ValidationError("Ви не можете залишити відгук на чужу книгу.")

        if shelf.status != 'finished':
            raise serializers.ValidationError("Відгук можна залишити тільки після прочитання книги.")

        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user