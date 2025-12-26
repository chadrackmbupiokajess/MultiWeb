from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Project, Subscriber

def index(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')

def services(request):
    return render(request, 'main/services.html')

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
