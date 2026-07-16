from django.db import models
from django.contrib.auth.models import User

from .managers import BookQuerySet

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    objects = BookQuerySet.as_manager()

    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Мої книжки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
