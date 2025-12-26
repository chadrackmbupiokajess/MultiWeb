from django.contrib import admin
from .models import Project, Subscriber

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('title',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    readonly_fields = ('subscribed_at',)
    search_fields = ('email',)
