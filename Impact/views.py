from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import *
from .forms import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def accueil(request):
    return render(request, 'siteweb/index.html')

def cursus(request):
    matricule = request.GET.get('matricule')
    
    student = get_object_or_404(Student, matricule=matricule)
    student_years = StudentYear.objects.filter(student=student).select_related('filiere', 'filiere__faculty', 'filiere__faculty__university')

    context = {
        'student': student,
        'student_years': student_years,
    }
    return render(request, 'siteweb/cursus.html', context)

def export_pdf(request, matricule):
    student = get_object_or_404(Student, matricule=matricule)
    student_years = StudentYear.objects.filter(student=student).select_related('filiere', 'filiere__faculty', 'filiere__faculty__university')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cursus_{student.matricule}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Title
    p.drawString(100, 750, f"Cursus de {student.name}")

    # Table headers
    y = 700
    p.drawString(50, y, "Université")
    p.drawString(150, y, "Faculté")
    p.drawString(250, y, "Filière")
    p.drawString(350, y, "Année d'étude")
    p.drawString(450, y, "Année académique")
    p.drawString(550, y, "Décision")

    # Table rows
    y -= 20
    for year in student_years:
        p.drawString(50, y, year.filiere.faculty.university.name)
        p.drawString(150, y, year.filiere.faculty.name)
        p.drawString(250, y, year.filiere.name)
        p.drawString(350, y, str(year.year))
        p.drawString(450, y, year.academic_year)
        decision = "Admis" if year.admitted else "Enjamber" if year.enjambed else "En attente" if year.current else "Redoubler"
        p.drawString(550, y, decision)
        y -= 20

    p.showPage()
    p.save()
    return response

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
                    # Go to a dashboard of university
                    return redirect('dashboard')
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

                secteurs_range = range(
                    faculte.nombre_secteur) if faculte.nombre_secteur > 1 else []

                form = CreateSecteursFilieresForm(faculte)

                context = {
                    'university': university,
                    'faculte': faculte,
                    'secteurs_range': secteurs_range,
                    'form': form,
                }
                return render(request, 'siteweb/Universite/create_facultes.html', context)

            except Faculty.DoesNotExist:
                messages.error(
                    request, 'Erreur lors de la création de la faculté')

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

            # Redirection après l'enregistrement des données
            return redirect('facultes')

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
            if Filiere.objects.filter(name=fil_name, faculty=faculte, sector=sector, delete=False).exists():
                messages.error(request, "Vous ne pouvez avoir deux filières avec le même nom dans la même faculté et/ou secteur. Veuillez vérifier et réessayer.")
            else:
                filiere = Filiere(name=fil_name, sigle=fil_sigle, faculty=faculte, sector=sector)
                filiere.save()

    # Redirection après l'enregistrement des données
    return redirect('facultes')

def filiere(request, fil_id):
    if 'university_id' not in request.session:
        return redirect('login')

    university_id = request.session.get('university_id')
    university = University.objects.get(id=university_id)

    filiere = Filiere.objects.get(id=fil_id)
    
    # Récupérer tous les ues de la filière et les classer par année
    ues_by_year = {}
    ues = UE.objects.filter(filiere=filiere, delete=False).order_by('year') 

    for ue in ues:
        year = ue.year

        if year not in ues_by_year:
            ues_by_year[year] = []

        ues_by_year[year].append(ue)

    # Récupérer tous les étudiants de la filière et les classer par année
    students_by_year = {}
    students = filiere.student_years_filieres.filter(Q(current=True) | Q(enjambed=True)).order_by('year')

    for student in students:
        year = student.year

        if year not in students_by_year:
            students_by_year[year] = []

        if not student.compo:
            student.statut = "En attente"
        elif student.admitted and student.enjambed:
            student.statut = "Enjambé"
        elif student.admitted and not student.enjambed:
            student.statut = "Admis"
        elif not student.admitted:
            student.statut = "Redouble"
        
        students_by_year[year].append(student)


    context = {
        'university': university,
        'faculty': filiere.faculty,
        'sector': filiere.sector,
        'filiere': filiere,
        'students_by_year': students_by_year,
        'ues_by_year': ues_by_year,
    }

    if request.method == 'POST':
        # Traitement du formulaire pour ajouter une nouvelle année avec des UEs
        year = request.POST.get('year')

        # Vérifier si des UEs existent déjà pour cette année et cette filière
        if UE.objects.filter(filiere=filiere, year=year).exists():
            messages.error(request, "Cette année existe déjà. Veuillez vérifier et réessayer.")
            messages.error(request, "Ou cliquez sur <<Gérer les UEs ici>> pour gérer les UEs de cette année")
            return redirect('filiere', fil_id=fil_id)

        ues = []

        for semester in range(1, 3):  # Boucle pour les deux semestres
            num_ue_semester = int(request.POST.get(f'num_ue_semester_{semester}'), 0)
            for i in range(1, num_ue_semester + 1):
                ue_name = request.POST.get(f'ue_name_{semester}_{i}')
                ue_sigle = request.POST.get(f'ue_sigle_{semester}_{i}')
                ue_credit = int(request.POST.get(f'ue_credit_{semester}_{i}'), 0)

                # Création des UEs et ajout à la liste
                ue = UE(name=ue_name, sigle=ue_sigle, filiere=filiere, year=year, semester=semester, credit=ue_credit)
                ue.save()
                ues.append(ue)

        # Redirection vers la même vue pour rafraîchir les données
        return redirect('filiere', fil_id=fil_id)

    return render(request, 'siteweb/Universite/filiere.html', context)

def edit_filiere(request, id):
    if 'university_id' not in request.session:
        return redirect('login')

    filiere = Filiere.objects.get(id=id)
    if filiere:
        if request.method == 'POST':
            filiere.name = request.POST.get('name')
            filiere.sigle = request.POST.get('sigle')
            filiere.save()
            messages.success(request, 'Filière mise à jour avec succès.')
        else:
            messages.error(request, 'Filière non mise à jour.')
    else:
        messages.error(request, 'Filière non mise à jour.')
        
    return redirect('facultes')

def delete_filiere(request, id):
    if 'university_id' not in request.session:
        return redirect('login')

    filiere = Filiere.objects.get(id=id)
    if filiere:
        filiere.delete = True
        filiere.save()
        messages.success(request, 'Filière supprimée avec succès.')
    else:
        messages.error(request, 'Filière non supprimée.')
        
    return redirect('facultes')

def manage_ue(request, fil_id, year):
    if 'university_id' not in request.session:
        return redirect('login')
    
    university_id = request.session.get('university_id')
    university = University.objects.get(id=university_id)
    
    filiere = Filiere.objects.get(id=fil_id)
    
    # Récupérer les ues de cette année et les classer par semestre
    ues_by_semester = {}
    ues = UE.objects.filter(filiere=filiere, year=year).order_by('semester')

    for ue in ues:
        semester = ue.semester

        if semester not in ues_by_semester:
            ues_by_semester[semester] = []

        ues_by_semester[semester].append(ue)
    
    if request.method == 'POST':
        type = request.POST.get('type')
        
        if type == 'ajout': # Gestion de l'ajout
            semester = request.POST.get('semester')
            name = request.POST.get('name')
            sigle = request.POST.get('sigle')
            credit = request.POST.get('credit')
            
            try:
                ue = UE(name=name, sigle=sigle, filiere=filiere, year=year, semester=semester, credit=credit)
                ue.save()
            except Exception as e:
                messages.error(request, 'Erreur d\'ajout de l\'UE')
                messages.error(request, str(e))
                
        elif type == 'edit': # Gestion de la modification
            try:
                ueId = request.POST.get('ueId')
                ue = UE.objects.get(id=ueId)

                ue.name = request.POST.get('name')
                ue.sigle = request.POST.get('sigle')
                ue.credit = request.POST.get('credit')
                ue.semester = request.POST.get('semester')
                ue.year = request.POST.get('year')
                
                ue.save()
                messages.success(request, 'UE mise à jour avec succès.')
            except Exception as e:
                messages.error(request, 'Erreur de modification de l\'UE')
                messages.error(request, str(e))
            
        elif type == 'delete': # Gestion de la suppression
            try:
                ueId = request.POST.get('ueId')
                ue = UE.objects.get(id=ueId)

                ue.delete = True
                
                ue.save()
                messages.success(request, 'UE supprimé avec succès.')
            except Exception as e:
                messages.error(request, 'Erreur de suppression de l\'UE')
                messages.error(request, str(e))
        
        return redirect('manage_ue', fil_id=fil_id, year=year)

    context = {
        'university': university,
        'faculty': filiere.faculty,
        'sector': filiere.sector,
        'filiere': filiere,
        'year': year,
        'ues_by_semester': ues_by_semester,
    }
    
    return render(request, 'siteweb/Universite/manage_ue.html', context)

def inscription(request):
    if 'university_id' not in request.session:
        return redirect('login')
    
    university_id = request.session['university_id']
    university = University.objects.get(id=university_id)
    
    faculties = Faculty.objects.filter(university=university)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        matricule = request.POST.get('matricule')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        filiere_id = request.POST.get('filiere')
        current_year = request.POST.get('current_year')
        academic_year = request.POST.get('academic_year')

        try:
            filiere = Filiere.objects.get(id=filiere_id)
            student, created = Student.objects.get_or_create(
                matricule=matricule,
                defaults={'name': name, 'email': email, 'telephone': telephone}
            )
            
            # Check if the student is already enrolled in the selected filiere
            if not student.filieres.filter(id=filiere_id).exists():
                student.filieres.add(filiere)

                StudentYear.objects.create(
                    student=student,
                    filiere=filiere,
                    year=current_year,
                    academic_year=academic_year,
                )
                    
                messages.success(request, f'Étudiant {student.matricule} inscrit avec succès.')
            elif not StudentYear.objects.filter(student=student, filiere=filiere, year=current_year).exists():
                StudentYear.objects.create(
                    student=student,
                    filiere=filiere,
                    year=current_year,
                    academic_year=academic_year,
                )
                
                messages.success(request, f'Étudiant {student.matricule} inscrit avec succès.')
            else:
                messages.warning(request, 'Cet étudiant est déjà inscrit dans cette filière.')

            return redirect('inscription')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'inscription: {e}')

    context = {
        'university': university,
        'faculties': faculties,
    }

    return render(request, 'siteweb/Universite/inscription.html', context)

def inscription_fil(request, fil_id):
    if 'university_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('ins_name')
        matricule = request.POST.get('ins_matricule')
        email = request.POST.get('ins_email')
        telephone = request.POST.get('ins_telephone')
        current_year = request.POST.get('ins_current_year')
        academic_year = request.POST.get('ins_academic_year')
        
        try:
            filiere = Filiere.objects.get(id=fil_id)
            student, created = Student.objects.get_or_create(
                matricule=matricule,
                defaults={'name': name, 'email': email, 'telephone': telephone}
            )
            
            # Check if the student is already enrolled in the selected filiere
            if not student.filieres.filter(id=fil_id).exists():
                student.filieres.add(filiere)

                StudentYear.objects.create(
                    student=student,
                    filiere=filiere,
                    year=current_year,
                    academic_year=academic_year,
                )
                    
                messages.success(request, f'Étudiant {student.matricule} inscrit avec succès.')
            elif not StudentYear.objects.filter(student=student, filiere=filiere, year=current_year).exists():
                StudentYear.objects.create(
                    student=student,
                    filiere=filiere,
                    year=current_year,
                    academic_year=academic_year,
                )
                
                messages.success(request, f'Étudiant {student.matricule} inscrit avec succès.')
            else:
                messages.warning(request, 'Cet étudiant est déjà inscrit dans cette filière.')

        except Exception as e:
            messages.error(request, f'Erreur lors de l\'inscription: {e}')

        return redirect('filiere', fil_id=fil_id)

def get_filieres(request, faculty_id):
    if 'university_id' not in request.session:
        return redirect('login')
    
    faculty = Faculty.objects.get(id=faculty_id)
    filieres = Filiere.objects.filter(faculty=faculty, delete=False)
    filieres_data = [{'id': filiere.id, 'name': filiere.name} for filiere in filieres]
    
    return JsonResponse({'filieres': filieres_data})

def get_years_fil(request, fil_id):
    if 'university_id' not in request.session:
        return redirect('login')
    
    filiere = Filiere.objects.get(id=fil_id)
    ues = UE.objects.filter(filiere=filiere).order_by('year')
    
    y_l = ["Première année", "Deuxième année", "Troisième année", "Quatrième année", "Cinquième année", "Sixième année", "Septième année"]
    year_fil = []
    year = []

    for ue in ues:
        if ue.year not in year:
            year.append(ue.year)
            year_fil.append({'value': ue.year, 'text': y_l[ue.year - 1]})
            
    return JsonResponse({'year_fil': year_fil})

def get_std_info(request, matricule):
    if 'university_id' not in request.session:
        return redirect('login')
    
    try:
        student = Student.objects.get(matricule=matricule)
        
        if student:
            return JsonResponse({'name': student.name, 'email': student.email, 'telephone': student.telephone})
        else:
            return JsonResponse({'name': "", 'email': "", 'telephone': ""})
    except Student.DoesNotExist:
        return JsonResponse({'name': "", 'email': "", 'telephone': ""})

def enter_grades(request, student_id, filiere_id, year):
    if 'university_id' not in request.session:
        return redirect('login')
    
    university_id = request.session['university_id']
    university = University.objects.get(id=university_id)
    
    student = Student.objects.get(id=student_id)
    filiere = Filiere.objects.get(id=filiere_id)
    ues = UE.objects.filter(filiere=filiere, year=year, delete=False).order_by('semester')
    
    ue_data = []
    for ue in ues:
        ue_info = {'ue': ue}
        if ue.grades.filter(student=student).exists():
            grade = ue.grades.get(student=student)
            ue_info['note'] = grade.score
            ue_info['valid'] = grade.score >= 60
        ue_data.append(ue_info)

    if request.method == 'POST':
        credit_total = 0
        credit_valid = 0
        
        st_y = StudentYear.objects.get(student=student, filiere=filiere, year=year, current=True)
        st_y.compo = True
        
        for ue_info in ue_data:
            ue = ue_info['ue']
            credit_total += ue.credit
            score = request.POST.get(f'score_{ue.id}')
            if score:
                Grade.objects.update_or_create(
                    student=student,
                    ue=ue,
                    defaults={'score': score}
                )
            
            if ue.grades.get(student=student).score >= 60:
                credit_valid += ue.credit
        
        if credit_total == credit_valid:
            st_y.admitted = True
            st_y.enjambed = False
        elif credit_valid >= credit_total * 0.8:
            st_y.enjambed = True
            st_y.admitted = True
        
        st_y.save()
                
        return redirect('filiere', fil_id=filiere_id)

    context = {
        'university': university,
        'student': student,
        'filiere': filiere,
        'faculty': filiere.faculty,
        'year': year,
        'ues': ue_data,
    }
    
    return render(request, 'siteweb/Universite/enter_grades.html', context)

def reinscribe_student(request, student_id, filiere_id, year):
    if 'university_id' not in request.session:
        return redirect('login')
    
    university_id = request.session['university_id']
    university = University.objects.get(id=university_id)
    
    student = Student.objects.get(id=student_id)
    filiere = Filiere.objects.get(id=filiere_id)
    
    student_year_c = StudentYear.objects.get(filiere=filiere, student=student, year=year, current=True)
    
    student_year_c.current = False
    student_year_c.save()
    
    next_start_year = int(student_year_c.academic_year.split('-')[1])
    next_academic_year = f"{next_start_year}-{next_start_year + 1}"
    
    if not student_year_c.admitted:
        student_year = StudentYear(filiere=filiere, year=year, student=student, academic_year=next_academic_year)
        student_year.save()
    elif UE.objects.filter(filiere=filiere, year=year + 1).exists():
        student_year = StudentYear(filiere=filiere, year=year+1, student=student, academic_year=next_academic_year)
        student_year.save()
    
    return redirect('filiere', fil_id=filiere_id)
