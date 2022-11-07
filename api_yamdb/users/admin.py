from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    search_fields = ('username', 'email')
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
