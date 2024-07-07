from django.urls import path
from . import views

urlpatterns = [
    # URLs User Interface
    path('', views.accueil, name='accueil'),
    path('cursusEtut', views.cursus, name='cursus'),
    
    # URLs University Interface
    path('login', views.login, name='login'),
    path('loginUni', views.university_login, name='loginP'),
    path('dashboard', views.dashboard, name='dashboard'), 
    path('facultes', views.facultes, name='facultes'),
    path('createFaculte', views.createFaculte, name='createFaculte'),
    path('create_secteurs_filieres', views.create_secteurs_filieres, name='create_secteurs_filieres'),
    path('add_filiere/<int:fac_id>', views.addfiliere, name='add_filiere'),
    path('filiere/<int:fil_id>', views.filiere, name='filiere'),
    path('edit_filiere/<int:id>/', views.edit_filiere, name='edit_filiere'),
    path('delete_filiere/<int:id>/', views.delete_filiere, name='delete_filiere'),
    path('manage_ue/<int:fil_id>/<int:year>/', views.manage_ue, name='manage_ue'),
    path('logout', views.logout, name='logout'),
]
