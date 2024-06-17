from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('cursusEtut', views.cursus, name='cursus'),
    path('login', views.login, name='login'),
    path('loginUni', views.university_login, name='loginP'),
    path('dashboard', views.dashboard, name='dashboard'), 
    path('facultes', views.facultes, name='facultes'),
    path('logout', views.logout, name='logout'),
]
