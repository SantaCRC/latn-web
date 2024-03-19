from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.forms import LoginForm, DocumentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile
import os

smart_str = lambda x: x

@login_required
def dashboard(request):
    try:
        name = request.user.get_full_name()
        role = request.user.groups.all()[0]
        return render(request, 'dashboard.html', {'name': name, 'role': role})
    except:
        return HttpResponseRedirect('/login/')

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
    check_is_user_exist_in_linux(user.username)
    if user.profile.key_is_active:
        return HttpResponseRedirect('/dashboard/')
    else:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend

        # generate private/public key pair
        key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
            key_size=2048)

        # get public key in OpenSSH format
        public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
            serialization.PublicFormat.OpenSSH)

        # get private key in PEM container format
        pem = key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        # decode to printable strings
        private_key_str = pem.decode('utf-8')
        public_key_str = public_key.decode('utf-8')

        print('Private key = ')
        print(private_key_str)
        # save private key to file
        filename = 'keys/' + user.username + '_private_key'
        with open(filename, 'wb') as file:
            file.write(private_key_str.encode('utf-8'))
            file.close()
        user.profile.key = filename
        user.profile.key_is_active = True
        user.profile.save()
        # install public key on server
        os.system('echo ' + public_key_str + ' >> ''/home/'+ user.username +'/.ssh/authorized_keys')
        
        
        
    
        print('Public key = ')
        print(public_key_str)


    return HttpResponseRedirect('/dashboard/')

def check_is_user_exist_in_linux(username):
    # check if user exists in linux if not create user
    if os.system('id -u ' + username) != 0:
        os.system('useradd -m ' + username)
        os.system('mkdir /home/' + username + '/.ssh')
        os.system('chown -R ' + username + ':' + username + ' /home/' + username + '/.ssh')
        os.system('chmod 700 /home/' + username + '/.ssh')
        os.system('touch /home/' + username + '/.ssh/authorized_keys')
        os.system('chown ' + username + ':' + username + ' /home/' + username + '/.ssh/authorized_keys')
        os.system('chmod 600 /home/' + username + '/.ssh/authorized_keys')
        os.system('systemctl restart sshd')
        os.system('useradd -D -g Participantes '+ username)
        return True
    else:
        return True