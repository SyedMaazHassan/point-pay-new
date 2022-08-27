import imp
from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def djangoAdminNotAllowed(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user
        if not profile.is_superuser:
             return function(request, *args, **kwargs)
        else:
            messages.error(request, "You are not allowed to access staff panel.")
            return redirect('authentication:logout')
    return wrap