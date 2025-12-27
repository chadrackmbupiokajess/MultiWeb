from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('manifest.webmanifest', main_views.manifest_view, name='manifest'),
    path('serviceworker.js', TemplateView.as_view(template_name='serviceworker.js', content_type='application/javascript'), name='serviceworker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'main.views.custom_500'
