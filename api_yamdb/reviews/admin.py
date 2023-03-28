from django.contrib import admin
from reviews.models import Title, Genre, Category, Review, Comment


class GenreInLine(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreInLine,)
    list_display = ('pk', 'name', 'year',
                    'description', 'get_genre', 'category')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date')
