from django.contrib import admin
# from django.contrib.admin import DateFieldListFilter

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display = ('username', 'first_name', 'last_name', 'created_at')
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ['username', 'first_name', 'last_name']
    # list_filter = (('created_at', DateFieldListFilter),)

# admin.site.register(User)
