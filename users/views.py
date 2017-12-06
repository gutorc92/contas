from django.shortcuts import render, redirect
from .forms import SigninForm, LoginForm, InvitationForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from contas.decorators import required_to_be_admin, required_to_be_student
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import FamilyRelationship
# Create your views here.


class MainView(View):
    
    def get(self, request):
        if self.request.user.is_authenticated():
            return redirect("index")
        else:
            redirect("loggin")
            

class LoginView(FormView):
    template_name = "users/signin.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        email, password = form.get_data()
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        else:
            form.add_error('password', 'Senha ou email inválidos')
            form.add_error('email', 'Senha ou email inválidos')
            return super(LoginView, self).form_invalid(form)         
        #return super(LoginView, self).form_valid(form)
        return redirect("logged")

    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return redirect("index")
        else:
            return super(LoginView, self).get(request)


class UserRegister(View):

    def get(self,request):
        if hasattr(request, 'user') and isinstance(request.user, get_user_model()):
            return redirect("index")
        else:
            form = SigninForm()
            return render(request, 'users/register.html', {'form': form})


    def post(self,request):
        form = SigninForm(request.POST)
        if form.is_valid():
           messages.success(request, u'Usuário criado com sucesso.')
           user = form.save()
           form = SigninForm()
        return render(request, 'users/register.html', {'form': form})

@method_decorator(required_to_be_admin, name="get")
class UserListView(View):
    
    def get(self, request):
        users_all = get_user_model().objects.all().exclude(id=request.user.pk)

        return render(request, 'users/users_list.html', {'list_all': users_all})


@method_decorator(required_to_be_admin, name="get")
class UserDeleteView(View):

    def get(self, request, id_user, action):
        if get_user_model().objects.filter(id=id_user).exists():
            user = get_user_model().objects.get(id=id_user)
            if action == "delete":
                messages.success(request, u'Usuário deletado com sucesso.')
                user.is_active = False
            elif action == "reactive":
                user.is_active = True
                messages.success(request, u'Usuário reativado com sucesso.')
            user.save()

        return redirect("list_users")

@method_decorator(required_to_be_admin, name="get")
class UserChangeGroupView(View):

    def get(self, request, id_user, group_change_to):
        if get_user_model().objects.filter(id=id_user).exists() and Group.objects.filter(name=group_change_to).exists():
            u = get_user_model().objects.get(id=id_user)
            group = Group.objects.get(name=group_change_to)
            if not u.hasGroup(group_change_to):
                u.groups.remove()
                u.groups.add(group)
                u.save()
            messages.success(request, u'Perfil trocado com sucesso!')

        return redirect("list_users")

class FamilyView(View):
    
    def get(self, request):
        family_list = request.user.family.all()
        return render(request, 'users/users_family.html', 
                {'family_list': family_list,
                 'form': InvitationForm()})

    def post(self, request):
        form = InvitationForm(request.POST)
        if form.is_valid() and form.save():
            form = InvitationForm()
        family_list = request.user.family.all()
        return render(request, 'users/users_family.html', 
                {'family_list': family_list,
                 'form': form})
class FamilyAcceptView(View):
        
    def get(self, request, id_invitation):
        if FamilyRelationship.objects.filter(pk=id_invitation).exists():
            fr = FamilyRelationship.objects.get(pk=id_invitation)
            if fr.user.pk == request.user.pk:
                fr.status = "1"
                fr.save()
                for frp in FamilyRelationship.objects.filter(user=request.user, status=3):
                    frp.delete()
                return redirect("family-list")
            else:
                return redirect("index")
        else:
            redirect("index")


