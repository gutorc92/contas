from contas.views import index
from functools import wraps
from django.contrib import messages

def required_to_be_logged(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Você não pode acessar a página')
            return index(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def required_to_be_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name="admin").exists() and request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You cannot access this page.')
            return index(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def required_to_be_student(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name="student").exists() and request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You cannot access this page.')
            return index(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

