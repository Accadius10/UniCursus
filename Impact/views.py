from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from .forms import *

def accueil(request):
    return render(request, 'siteweb/index.html')

def cursus(request):
    return render(request, 'siteweb/cursus.html')

# Université
def login(request):
    if 'university_id' in request.session:
        return redirect('dashboard')

    form = LoginForm()
    return render(request, 'siteweb/Login.html', {'form': form})

def university_login(request):
    if 'university_id' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                university = University.objects.get(email=email)

                if university.check_password(password):
                    # Log the user in (you can use sessions)
                    request.session['university_id'] = university.id
                    return redirect('dashboard')  # Go to a dashboard of university
                else:
                    messages.error(request, 'Invalid email or password')

            except University.DoesNotExist:
                messages.error(request, 'Invalid email or password')

    else:
        form = LoginForm()

    return render(request, 'siteweb/Login.html', {'form': form})

def logout(request):
    if 'university_id' in request.session:
        del request.session['university_id']

    return redirect('login')

def dashboard(request):
    if 'university_id' not in request.session:
        return redirect('login')

    # Retrieve university information
    university_id = request.session['university_id']
    university = University.objects.get(id=university_id)
    return render(request, 'siteweb/Universite/dashboard.html', {'university': university})

def facultes(request):
    if 'university_id' not in request.session:
        return redirect('login')

    if 'faculte_id' in request.session:
        del request.session['faculte_id']
    
    # Retrieve university information
    university_id = request.session['university_id']
    university = University.objects.get(id=university_id)

    faculties = university.faculties.all()

    form = CreateFacultyForm()

    context = {
        'university': university,
        'faculties': faculties,
        'form': form
    }
        
    return render(request, 'siteweb/Universite/facultes.html', context)

def createFaculte(request):
    if 'university_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = CreateFacultyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            isFaculte = form.cleaned_data['isFaculte']
            nombre_secteur = form.cleaned_data['nombre_secteur']

            try:
                university_id = request.session['university_id']
                university = University.objects.get(id=university_id)

                faculte = Faculty(name=name, isFaculte=isFaculte, nombre_secteur=nombre_secteur, university=university)
                faculte.save()

                request.session['faculte_id'] = faculte.id

                secteurs_range = range(faculte.nombre_secteur) if faculte.nombre_secteur > 1 else []
                print(secteurs_range)
                context = {
                    'university': university,
                    'faculte': faculte,
                    'secteurs_range': secteurs_range,
                }
                return render(request, 'siteweb/Universite/create_facultes.html', context)

            except Exception as e:
                messages.error(request, 'Erreur lors de la création de la faculté ' + str(e))
        else:
            messages.error(request, 'Formulaire invalide')
            form = CreateFacultyForm()

    else:
        form = CreateFacultyForm()

    return redirect('facultes')

def create_secteurs_filieres(request):
    if 'university_id' not in request.session:
        return redirect('login')

    faculte_id = request.session.get('faculte_id')
    faculte = Faculty.objects.get(id=faculte_id)

    if request.method == 'POST':
        form = CreateSecteursFilieresForm(faculte, request.POST)
        if form.is_valid():
            if faculte.nombre_secteur > 1:
                for i in range(faculte.nombre_secteur):
                    secteur_name = form.cleaned_data[f'secteur_{i}_name']
                    nombre_filieres = form.cleaned_data[f'nombre_filieres_{i}']

                    secteur = Sector(name=secteur_name, faculty=faculte)
                    secteur.save()

                    for j in range(nombre_filieres):
                        filiere_name = form.cleaned_data[f'filiere_{i}_{j}_name']
                        filiere = Filiere(name=filiere_name, sector=secteur, faculty=faculte)
                        filiere.save()
            else:
                nombre_filieres = form.cleaned_data['nombre_filieres']

                for i in range(nombre_filieres):
                    filiere_name = form.cleaned_data[f'filiere_{i}_name']
                    filiere = Filiere(name=filiere_name, faculty=faculte)
                    filiere.save()

            return redirect('facultes')  # Redirection après l'enregistrement des données

    else:
        form = CreateSecteursFilieresForm(faculte)

    context = {
        'form': form,
        'faculte': faculte,
        'university': faculte.university,
    }
    return render(request, 'siteweb/Universite/create_secteurs_filieres.html', context)

