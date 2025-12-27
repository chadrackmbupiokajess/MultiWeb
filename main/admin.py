from django.contrib import admin
from .models import Project, Subscriber, NavigationItem, SiteSettings, Service

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_public', 'is_pinned')
    list_filter = ('is_public', 'is_pinned')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'date', 'is_public', 'is_pinned', 'link')
        }),
        ('Images', {
            'fields': ('image', 'mobile_image')
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    readonly_fields = ('subscribed_at',)
    search_fields = ('email',)

@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order')
    list_editable = ('order',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Général', {
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('Page d\'accueil', {
            'fields': ('hero_description',)
        }),
        ('Page À Propos', {
            'fields': ('about_title', 'about_description', 'about_image')
        }),
        ('PWA', {
            'fields': ('pwa_icon_192', 'pwa_icon_512')
        }),
    )

    def has_add_permission(self, request):
        # Empêche l'ajout de nouvelles instances si une existe déjà
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Empêche la suppression de l'instance
        return False
