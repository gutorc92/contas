from django.shortcuts import render
from .models import Category,Statement,StatementType
from .forms import CategoryForm,StatementForm,StatementTypeForm
from django.views import View
# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
import datetime

class DashBoard(View):

    def get(self, request):
        result = StatementType.objects.sum_by_range(request.user.pk)
        result_category = Category.objects.sum_by_range(request.user.pk, 1).values_list('description', 'total')
        result_list = ()
        for st in result:
            result_list = result_list + ((st.description, st.total, st.get_color()),)
        return render(request, "blue/dashboard.html",{
                "month" : datetime.datetime.now().strftime("%B"),
                "list_st": result_list,
                "list_ct": result_category})

class StatementListView(View):

    def get(self, request):
        statements = Statement.objects.filter(user__id = request.user.pk).order_by('-date')
        return  render(request,"blue/statement_list.html",{ 
            'statements': statements})
        
class StatementView(View):

    def get(self, request, id_type):
        if StatementType.objects.filter(id=id_type).exists():
            statements = Statement.objects.filter(st_type__pk=id_type, 
                    user__id = request.user.pk)
            categories = Category.objects.filter(family__members__id=request.user.pk)
            form = StatementForm(initial={'st_type': id_type, 'categories': categories})
            return  render(request,"blue/statement.html",{'form':form, 
                'id_type': id_type,
                'type_name': StatementType.objects.get(id=id_type).description,
                'statements': statements})
        else:
            return redirect("index")

    def post(self, request, id_type):
        form = StatementForm(request.POST)
        statements = Statement.objects.filter(st_type__pk=id_type, 
                    user__id = request.user.pk)
        categories = Category.objects.filter(family__members__id=request.user.pk)
        if form.is_valid() and form.save(request.user):
            form = StatementForm(initial={'st_type': id_type, 'categories': categories})
        return  render(request,"blue/statement.html",{'form':form, 
                'id_type': id_type,
                'statements': statements})


class CategoryCreate(View):
    model = Category
    form_class = CategoryForm
    template_name  = "blue/category.html"
    
    def get(self, request):
        categories = Category.objects.filter(family__members__id=request.user.pk)
        return  render(request,"blue/category.html",{'form': self.form_class, 
                'categories': categories })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request.user)
            form = self.form_class()

        categories = Category.objects.filter(family__members__id=request.user.pk)
        return  render(request,"blue/category.html",{'form': self.form_class, 
                'categories': categories })

class CategoryUpdate(UpdateView):
    model = Category
    fields = ['description']

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('category')



def create_statement_type(request):
    if request.method == 'POST':
        form = StatementTypeForm(request.POST)
        if form.is_valid() and form.save():
            form = StatementTypeForm()
    else:
        form = StatementTypeForm()
    statements_type = StatementType.objects.all()
    return  render(request,"blue/statement_type.html",{'form':form, 'st_types': statements_type})
