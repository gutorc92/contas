from django.shortcuts import render
from .models import Category,Statement,StatementType
from .forms import CategoryForm,StatementForm,StatementTypeForm
# Create your views here.

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid() and form.save():
            form = CategoryForm()
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return  render(request,"blue/category.html",{'form':form, 'categories': categories})

def create_statement(request):
    if request.method == 'POST':
        form = StatementForm(request.POST)
        if form.is_valid() and form.save():
            form = StatementForm()
    else:
        form = StatementForm()
    statements = Statement.objects.all()
    return  render(request,"blue/statement.html",{'form':form, 'statements': statements})

def create_statement_type(request):
    if request.method == 'POST':
        form = StatementTypeForm(request.POST)
        if form.is_valid() and form.save():
            form = StatementTypeForm()
    else:
        form = StatementTypeForm()
    statements_type = StatementType.objects.all()
    return  render(request,"blue/statement_type.html",{'form':form, 'st_types': statements_type})
