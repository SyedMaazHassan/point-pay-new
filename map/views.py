from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.supporting_func import *
from dashboard.supporting_func import getUser
from drivers.forms import *
from authentication.decorators import djangoAdminNotAllowed

# Create your views here.
@djangoAdminNotAllowed
@login_required
def monitor(request):
    context = {"page": "monitor"}
    return render(request, "home/map.html", context)
