from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.forms import LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

@login_required
def dashboard(request):
    name = request.user.get_full_name()
    role = request.user.groups.all()[0]
    return render(request, 'dashboard.html', {'name': name, 'role': role})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = username.lower()
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            return HttpResponseRedirect('/dashboard/')
        else:
            # Invalid login, render login page with form
            form = LoginForm()
            error = 1
            return render(request, 'login.html', {'form': form, 'error':  error})
    else:
        # Render the login page with form
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
