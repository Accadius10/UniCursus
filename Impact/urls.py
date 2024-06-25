from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('cursusEtut', views.cursus, name='cursus'),
    path('login', views.login, name='login'),
    path('loginUni', views.university_login, name='loginP'),
    path('dashboard', views.dashboard, name='dashboard'), 
    path('facultes', views.facultes, name='facultes'),
    path('createFaculte', views.createFaculte, name='createFaculte'),
    path('create_secteurs_filieres', views.create_secteurs_filieres, name='create_secteurs_filieres'),
    path('add_filiere/<int:fac_id>', views.addfiliere, name='add_filiere'),
    path('filiere/<int:fil_id>', views.filiere, name='filiere'),
    path('logout', views.logout, name='logout'),
]
