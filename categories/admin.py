from django.contrib import admin
from .models import category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']  # Set up the field for autocomplete

admin.site.register(category, CategoryAdmin)

