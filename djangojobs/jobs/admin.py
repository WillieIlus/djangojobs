from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'category', 'openings', 'duration_days')
    list_display_links = ('title',)
    list_filter = ('category', 'location')  # 'opening')
    search_fields = ('title', 'description', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_on',)
