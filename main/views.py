from django.shortcuts import render, redirect, get_object_or_404
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

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project}
    return render(request, 'main/project_detail.html', context)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Redirige vers la page d'origine, ou l'accueil par défaut
        redirect_url = request.META.get('HTTP_REFERER', '/')

        if not email:
            messages.error(request, 'Veuillez fournir une adresse e-mail.')
            return redirect(redirect_url)

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Adresse e-mail invalide.')
            return redirect(redirect_url)

        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, 'Vous êtes déjà abonné à notre newsletter.')
            return redirect(redirect_url)
        
        Subscriber.objects.create(email=email)
        messages.success(request, 'Merci pour votre inscription ! Vous recevrez nos prochaines publications.')
    
    # Redirige vers la page d'origine après le traitement
    return redirect(redirect_url)
