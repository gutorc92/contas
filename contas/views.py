from django.shortcuts import render
from django.views import View
# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    return render(request, 'contas/base.html')
