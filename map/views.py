from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from dashboard.supporting_func import *
from drivers.models import Driver
from dashboard.supporting_func import getUser
from django.contrib import messages
from drivers.forms import *
from django.views.generic import ListView

# Create your views here.
@login_required
def monitor(request):
    context = {"page": "monitor"}
    return render(request, "home/map.html", context)
