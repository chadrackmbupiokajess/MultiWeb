from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accueil/', views.index, name='accueil'),
    path('a-propos/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('projet/<slug:slug>/', views.project_detail, name='project_detail'),
    path('inscription/', views.subscribe, name='subscribe'),
    path('offline/', views.offline_view, name='offline'),
]
