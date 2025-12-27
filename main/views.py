from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Project, Subscriber, SiteSettings, Service
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage

def index(request):
    project_list = Project.objects.order_by('-is_pinned', '-date')
    paginator = Paginator(project_list, 6) # 6 projets par page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')

def services(request):
    services_list = Service.objects.all()
    context = {'services': services_list}
    return render(request, 'main/services.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        from_email = request.POST.get('email')
        message_body = request.POST.get('message')

        full_message = f"""Message reçu de : {name} ({from_email})\n\n{message_body}\n"""

        try:
            send_mail(
                f'Message de {name} via le portfolio',  # Sujet
                full_message,  # Message
                settings.EMAIL_HOST_USER,  # De (votre email configuré)
                [settings.EMAIL_HOST_USER],  # À (votre propre email)
                fail_silently=False,
            )
            messages.success(request, 'Votre message a bien été envoyé ! Merci.')
        except Exception as e:
            messages.error(request, f'Une erreur est survenue. {e}')

        return redirect('contact')

    return render(request, 'main/contact.html')

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {'project': project}
    return render(request, 'main/project_detail.html', context)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Veuillez fournir une adresse e-mail.'}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Adresse e-mail invalide.'}, status=400)

        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'status': 'info', 'message': 'Vous êtes déjà abonné.'})
        
        Subscriber.objects.create(email=email)
        return JsonResponse({'status': 'success', 'message': 'Merci ! Inscription réussie.'})
    
    return JsonResponse({'status': 'error', 'message': 'Requête invalide.'}, status=405)

def custom_500(request):
    return render(request, '500.html', status=500)

def manifest_view(request):
    settings = SiteSettings.load()
    manifest = {
        "name": settings.site_name,
        "short_name": settings.site_name,
        "id": "/?source=pwa",
        "start_url": "/",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#ffffff",
        "theme_color": "#2D1D7A",
        "description": settings.hero_description,
        "icons": []
    }
    if settings.pwa_icon_192:
        manifest["icons"].append({
            "src": settings.pwa_icon_192.url,
            "sizes": "192x192",
            "type": "image/png"
        })
    if settings.pwa_icon_512:
        manifest["icons"].append({
            "src": settings.pwa_icon_512.url,
            "sizes": "512x512",
            "type": "image/png"
        })
    return JsonResponse(manifest)

def offline_view(request):
    return render(request, 'offline.html')

def serviceworker_view(request):
    settings_obj = SiteSettings.load()
    
    # URLs de base à mettre en cache
    cache_urls = [
        reverse('index'),
        reverse('accueil'),
        reverse('about'),
        reverse('services'),
        reverse('contact'),
        reverse('offline'),
        staticfiles_storage.url('images/favicon.ico'), # Fallback favicon
        staticfiles_storage.url('images/logo.ico'), # Fallback logo
    ]

    # Ajouter les images dynamiques si elles existent
    if settings_obj.logo:
        cache_urls.append(settings_obj.logo.url)
    if settings_obj.favicon:
        cache_urls.append(settings_obj.favicon.url)
    if settings_obj.pwa_icon_192:
        cache_urls.append(settings_obj.pwa_icon_192.url)
    if settings_obj.pwa_icon_512:
        cache_urls.append(settings_obj.pwa_icon_512.url)

    # Rendre le template du Service Worker avec la liste des URLs
    response = render(request, 'serviceworker.js', {'cache_urls': cache_urls}, content_type='application/javascript')
    return response
