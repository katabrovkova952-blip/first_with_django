from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from .managers import BookQuerySet


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_pages = models.PositiveIntegerField()

    objects = BookQuerySet.as_manager()

    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_page = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ("to_read", "Хочу прочитати"),
        ("reading", "Читаю"),
        ("finished", "Прочитано"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to_read")

    class Meta:
       constraints = [
           models.UniqueConstraint(
               fields=['user', 'book'],
               name='unique_user_book'
           )
       ]

    def save(self, *args, **kwargs):
        if self.status == 'finished' and self.finished_at is None:
            self.finished_at = timezone.now()
        super().save(*args, **kwargs)


class Review(models.Model):
    shelf = models.OneToOneField(Shelf, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    @property
    def user(self):
        return self.shelf.user
    