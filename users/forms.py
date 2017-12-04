from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.core.validators import validate_integer, RegexValidator
from .models import Family

class LoginForm(forms.Form):

    email = forms.EmailField(
        label=_('Email:'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}),
        error_messages={'invalid': _('Email address must \
                                       be in a valid format.')})
    password = forms.CharField(
        label=_('Senha:'),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))



    def get_data(self):
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        return username, password 


class SigninForm(forms.Form):
    name = forms.CharField(label='Nome completo',
        required=True) 
    email = forms.CharField(label='Email',
        required=True)
    password = forms.CharField(label='Senha',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme '}))
    password_confirm = forms.CharField(label='Senha',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha '}))
    
    

    def clean(self):
        cleaned_data = super(SigninForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")

        user_model =  get_user_model()
        if user_model.objects.filter(email=email).exists():
            raise ValidationError("O email ja esta cadastrado") 
        
        val = RegexValidator('^[a-zA-Z0-9\s]*$', message='O nome nao pode ter caracteres especiais como *, &, etc.')
        if len(name) < 3:
            msg = "O nome não pode ser nulo"
            self.add_error('first_name', msg)
        if len(password) < 8 or (password != password_confirm):
            msg = "Senhas precisam ser iguais ou maiores que oito"
            self.add_error('password', msg)
            self.add_error('password_confirm', msg)
        return cleaned_data

    def save(self, commit=True):
        user = get_user_model()() 
        cleaned_data = super(SigninForm, self).clean()
        names = cleaned_data.get("name").split()
        user.fisrt_name = names[0]
        del names[0]
        user.last_name = " ".join(names)
        user.email = cleaned_data.get("email")
        user.set_password(cleaned_data.get("password"))
        user.save() 
        family = self.create_family(names) 
        user.family.add(family)
        user.save() 
        
    def create_family(self, names):
        family = Family()
        family.name = names[-1];
        family.save()
        return family
