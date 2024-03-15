import django.forms
from django.forms import ModelForm
from .models import User, Document

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': django.forms.PasswordInput(),
        }
        
class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']