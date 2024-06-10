from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import University
from .forms import LoginForm

def accueil(request):
    return render(request, 'siteweb/index.html')

def login(request):
    return render(request, 'siteweb/Login.html')

def cursus(request):
    return render(request, 'siteweb/cursus.html')

def university_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                university = University.objects.get(username=username)
                if university.check_password(password):
                    # Log the user in (you can use sessions)
                    request.session['university_id'] = university.id
                    return redirect('dashboard',)  # Redirect to a dashboard or home page
                else:
                    messages.error(request, 'Invalid username or password')
            except University.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'siteweb/Login.html', {'form': form})

def dashboard(request):
    if 'university_id' not in request.session:
        return redirect('login')
    # Retrieve university information
    university_id = request.session['university_id']
    university = University.objects.get(id=university_id)
    return render(request, 'siteweb/Universite/dashboard.html', {'university': university})