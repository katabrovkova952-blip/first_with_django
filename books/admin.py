from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('is_published', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('is_published',)
    list_display_links = ('title',)
    list_per_page = 20