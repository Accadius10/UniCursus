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
                    messages.error(request, 'E-mail ou mot de passe invalide')

            except University.DoesNotExist:
                messages.error(request, 'E-mail ou mot de passe invalide')

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

    faculties = university.faculties.all().order_by('name')

    form = CreateFacultyForm()
    
    formA = AddFiliereForm()

    context = {
        'university': university,
        'faculties': faculties,
        'form': form,
        'formA': formA,
    }
        
    return render(request, 'siteweb/Universite/facultes.html', context)

def createFaculte(request):
    if 'university_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = CreateFacultyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sigle = form.cleaned_data['sigle']
            isFaculte = form.cleaned_data['isFaculte']
            nombre_secteur = form.cleaned_data['nombre_secteur']

            try:
                university_id = request.session['university_id']
                university = University.objects.get(id=university_id)

                faculte = Faculty(name=name, sigle=sigle, isFaculte=isFaculte, nombre_secteur=nombre_secteur, university=university)
                faculte.save()

                request.session['faculte_id'] = faculte.id

                secteurs_range = range(faculte.nombre_secteur) if faculte.nombre_secteur > 1 else []
                
                form = CreateSecteursFilieresForm(faculte)

                context = {
                    'university': university,
                    'faculte': faculte,
                    'secteurs_range': secteurs_range,
                    'form': form,
                }
                return render(request, 'siteweb/Universite/create_facultes.html', context)

            except Faculty.DoesNotExist:
                messages.error(request, 'Erreur lors de la création de la faculté')

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
                        filiere_sigle = form.cleaned_data[f'filiere_{i}_{j}_sigle']
                        filiere = Filiere(name=filiere_name, sigle=filiere_sigle, sector=secteur, faculty=faculte)
                        filiere.save()
            else:
                secteur = Sector(name=faculte.name, faculty=faculte)
                secteur.save()

                nombre_filieres = form.cleaned_data['nombre_filieres']

                for i in range(nombre_filieres):
                    filiere_name = form.cleaned_data[f'filiere_{i}_name']
                    filiere_sigle = form.cleaned_data[f'filiere_{i}_sigle']
                    filiere = Filiere(name=filiere_name, sigle=filiere_sigle, sector=secteur, faculty=faculte)
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

def addfiliere(request, fac_id):
    if 'university_id' not in request.session:
        return redirect('login')
    
    faculte = Faculty.objects.get(id=fac_id)
    
    if request.method == 'POST':
        form = AddFiliereForm(request.POST)
        
        if form.is_valid():
            sector_name = form.cleaned_data['name_sector']
            fil_name = form.cleaned_data['name']
            fil_sigle = form.cleaned_data['sigle']
            
            # Vérifier si le secteur existe déjà
            try:
                sector = Sector.objects.get(name=sector_name, faculty=faculte)
            except Sector.DoesNotExist:
                sector = Sector(name=sector_name, faculty=faculte)
                sector.save()
                
                faculte.nombre_secteur += 1
                faculte.save()
                
            # Vérifier si cette filière existe déjà dans cette faculté
            if Filiere.objects.filter(name=fil_name, faculty=faculte, sector=sector).exists():
                messages.error(request, "Vous ne pouvez avoir deux filières avec le même nom dans la même faculté et/ou secteur. Veuillez vérifier et réessayer.")
            else:
                filiere = Filiere(name=fil_name, sigle=fil_sigle, faculty=faculte, sector=sector)
                filiere.save()
    
    return redirect('facultes') # Redirection après l'enregistrement des données

def filiere(request, fil_id):
    if 'university_id' not in request.session:
        return redirect('login')

    university_id = request.session.get('university_id')
    university = University.objects.get(id=university_id)

    filiere = Filiere.objects.get(id=fil_id)

    # Récupérer tous les étudiants de la filière et les classer par année
    students_by_year = {}
    students = filiere.students.order_by('current_year')

    for student in students:
        year = student.current_year

        if year not in students_by_year:
            students_by_year[year] = []

        students_by_year[year].append(student)

    context = {
        'university': university,
        'faculty': filiere.faculty,
        'sector': filiere.sector,
        'filiere': filiere,
        'students_by_year': students_by_year,
    }

    if request.method == 'POST':
        # Traitement du formulaire pour ajouter une nouvelle année avec des UEs
        year = request.POST.get('year')

        # Vérifier si des UEs existent déjà pour cette année et cette filière
        if UE.objects.filter(filiere=filiere, year=year).exists():
            messages.error(request, f"Des UEs existent déjà pour cette année. Veuillez vérifier et réessayer.")
            return redirect('filiere', fil_id=fil_id)

        ues = []

        for semester in range(1, 3):  # Boucle pour les deux semestres
            num_ue_semester = int(request.POST.get(f'num_ue_semester_{semester}'))
            for i in range(1, num_ue_semester + 1):
                ue_name = request.POST.get(f'ue_name_{semester}_{i}')
                ue_sigle = request.POST.get(f'ue_sigle_{semester}_{i}')
                ue_credit = request.POST.get(f'ue_credit_{semester}_{i}')

                # Création des UEs et ajout à la liste
                ue = UE.objects.create(name=ue_name, sigle=ue_sigle, filiere=filiere, year=year, semester=semester, credit=ue_credit)
                ues.append(ue)

        # Redirection vers la même vue pour rafraîchir les données
        return redirect('filiere', fil_id=fil_id)

    return render(request, 'siteweb/Universite/filiere.html', context)
