from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
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
        email = request.POST.get('email')
        message_body = request.POST.get('message')

        # Envoyer l'e-mail (qui s'affichera dans la console)
        send_mail(
            f'Message de {name} via le portfolio',  # Sujet
            message_body,  # Message
            email,  # De (email de l'expéditeur)
            ['votre_email@example.com'],  # À (votre adresse e-mail de réception)
        )

        messages.success(request, 'Votre message a bien été envoyé ! Merci.')
        return redirect('contact')

    return render(request, 'main/contact.html')
