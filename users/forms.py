from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.core.validators import validate_integer, RegexValidator
from .models import FamilyRelationship, Family
from django.core.exceptions import ValidationError

class InvitationForm(forms.Form):

    email = forms.EmailField(
        label=_('Email:'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}),
        error_messages={'invalid': _('Email address must \
                                       be in a valid format.')})
    family = forms.CharField(
        required=True,
        widget=forms.HiddenInput())

    def clean(self):
        username = self.cleaned_data.get("email")
        family = self.cleaned_data.get("family")
        user_model =  get_user_model()
        if not user_model.objects.filter(email=username).exists():
            raise ValidationError(_("Email not found")) 
        user = get_user_model().objects.get(email=username)
        if not Family.objects.filter(pk=family).exists():
            raise ValidationError(_("Family not found"))
        if FamilyRelationship.objects.filter(user=user, family_id=family).exists():
            raise ValidationError(_("RelationShip already exists"))
            
    def save(self):
        username = self.cleaned_data.get("email")
        family = self.cleaned_data.get("family")
        fr = FamilyRelationship()
        fr.user = get_user_model().objects.get(email=username)
        fr.family = Family.objects.get(pk=family)
        fr.status = "2"
        fr.save()
        return fr 



class LoginForm(forms.Form):

    email = forms.EmailField(
        label=_('Email:'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}),
        error_messages={'invalid': _('Email address must \
                                       be in a valid format.')})
    password = forms.CharField(
        label=_('Password:'),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))



    def get_data(self):
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        return username, password 


class SigninForm(forms.Form):
    name = forms.CharField(label=_('Complete Name'),
        required=True) 
    email = forms.CharField(label='Email',
        required=True)
    password = forms.CharField(label=_('Password'),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': _('Your password ')}))
    password_confirm = forms.CharField(label=_('Password Confirm'),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm your password')}))
    
    

    def clean(self):
        cleaned_data = super(SigninForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")

        user_model =  get_user_model()
        if user_model.objects.filter(email=email).exists():
            raise ValidationError(_("Email already registered")) 
        
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
        user.first_name = names[0]
        del names[0]
        user.last_name = " ".join(names)
        user.email = cleaned_data.get("email")
        user.set_password(cleaned_data.get("password"))
        user.save() 
        family = self.create_family(names) 
        family.user = user
        family.save() 
        
    def create_family(self, names):
        family = Family()
        family.name = names[-1];
        family.save()
        family_relation = FamilyRelationship()
        family_relation.family = family 
        family_relation.status = "3"
        return family_relation
