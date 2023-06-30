from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'created_at')
    list_filter = ('category', 'location')
    search_fields = ('name', 'description', 'address', 'website', 'twitter', 'email')
    prepopulated_fields = {'slug': ('name',)}
