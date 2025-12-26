from .models import NavigationItem, SiteSettings

def navigation_items(request):
    return {
        'nav_items': NavigationItem.objects.all()
    }

def site_settings(request):
    return {
        'site_settings': SiteSettings.load()
    }
