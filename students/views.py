from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from dashboard.supporting_func import *
from dashboard.models import *
from dashboard.supporting_func import getUser
from django.contrib import messages

def getAllStudents(organization):
    return Voucher.objects.filter(organization = organization)

@login_required
def students(request):
    user = getUser(request.user)
    context = {'page': 'students', 'all_vouchers': getAllStudents(user.organization)}
    return render(request, "home/students.html", context)


@login_required
def single_student(request, voucher_id):
    user = getUser(request.user)
    context = {'page': 'vouchers', 'all_vouchers': getAllStudents(user.organization)}
    # my voucher
    voucher = Voucher.objects.filter(id = voucher_id, organization = user.organization).first()
    if voucher:
        context['single_voucher'] = voucher
    else:
        messages.error(request, "Voucher doesn't exist with this id OR you don't have access")
        return redirect('vouchers:all')
    return render(request, "home/vouchers.html", context)