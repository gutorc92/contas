from django.shortcuts import render
from .models import Category,Statement,StatementType
from .forms import CategoryForm,StatementForm,StatementTypeForm
from django.views import View
# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class StatementView(View):

    def get(self, request, id_type):
        if StatementType.objects.filter(id=id_type).exists():
            statements = Statement.objects.all()
            form = StatementForm(initial={'st_type': id_type})
            return  render(request,"blue/statement.html",{'form':form, 
                'id_type': id_type,
                'statements': statements})


    def post(self, request, id_type):
        form = StatementForm(request.POST)
        statements = Statement.objects.all()
        if form.is_valid() and form.save():
            form = StatementForm(initial={'st_type': id_type})
        return  render(request,"blue/statement.html",{'form':form, 
                'id_type': id_type,
                'statements': statements})


class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name  = "category.html"
    #extra_context['categories'] = Category.objects.all()

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
