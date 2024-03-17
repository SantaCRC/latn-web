from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.forms import LoginForm, DocumentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile
import paramiko

smart_str = lambda x: x

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

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = DocumentForm()
    return render(request, 'form-elements.html', {'form': form})

@login_required
def download_key_file(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    key = profile.key
    if key:
        response = HttpResponse(key, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(key)
        return response
    else:
        return HttpResponseRedirect('/dashboard/')
    
@login_required
def VM(request):
    return render(request, 'vm.html')

@login_required
def generate_key(request):
    user = request.user
    if user.profile.key_is_active:
        return HttpResponseRedirect('/dashboard/')
    else:
        key = paramiko.RSAKey.generate(2048)

        # Get the public and private keys as strings
        private_key = key.get_private_key().decode('utf-8')
        public_key = key.get_base64()

        print(private_key)
        print(public_key)
    return HttpResponseRedirect('/dashboard/')
