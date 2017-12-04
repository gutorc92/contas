from django.shortcuts import render
from .models import Category,Statement,StatementType
from .forms import CategoryForm,StatementForm,StatementTypeForm
from django.views import View
# Create your views here.


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

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid() and form.save():
            form = CategoryForm()
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return  render(request,"blue/category.html",{'form':form, 'categories': categories})

def create_statement_type(request):
    if request.method == 'POST':
        form = StatementTypeForm(request.POST)
        if form.is_valid() and form.save():
            form = StatementTypeForm()
    else:
        form = StatementTypeForm()
    statements_type = StatementType.objects.all()
    return  render(request,"blue/statement_type.html",{'form':form, 'st_types': statements_type})
