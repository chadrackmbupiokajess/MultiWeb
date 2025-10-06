from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project

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

        # Construire le message complet
        full_message = f"""Message reçu de : {name} ({from_email})

{message_body}
"""

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
