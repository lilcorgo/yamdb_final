from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
    )
    list_editable = 'role',
    search_fields = 'username',
    list_filter = 'role',
    empty_value_display = '-пусто-'
