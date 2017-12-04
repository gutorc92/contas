from django.shortcuts import render, redirect
from .forms import SigninForm, LoginForm
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
# Create your views here.


class MainView(View):
    
    def get(self, request):
        if request.user.is_authenticated():
            return CardListView.as_view()(self.request, "my")
        else:
            redirect("loggin")
            

class LoginView(FormView):
    template_name = "users/signin.html"
    form_class = LoginForm
    success_url = "/cards/all"

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
        if not request.user.is_authenticated():
            return super(LoginView, self).get(request)
        else:
            logout(self.request)
            return redirect("index")


class UserRegister(View):

    def get(self,request):
        if not request.user.is_authenticated():
            print("Aqui")
            form = SigninForm()
            return render(request, 'students/signin.html', {'form': form})
        else:
            return redirect("index")

    def post(self,request):
        form = SigninForm(request.POST)
        if form.is_valid():
           messages.success(request, u'Usuário criado com sucesso.')
           user = form.save()
           form = SigninForm()
        return render(request, 'students/signin.html', {'form': form})

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
