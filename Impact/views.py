from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import University
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