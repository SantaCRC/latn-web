from django.shortcuts import render

# simple dashboard view
def dashboard(request):
    return render(request, 'dashboard.html', {})

