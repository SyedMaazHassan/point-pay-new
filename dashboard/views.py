from django.contrib.auth.decorators import login_required
from dashboard.supporting_func import *
from dashboard.models import *
from django.shortcuts import render, redirect
from authentication.decorators import djangoAdminNotAllowed
from django.contrib import messages
from django.db import transaction

@djangoAdminNotAllowed
@login_required
def index(request):
    user = getUser(request.user)
    my_datetime = timezone.now().strftime("%B, %Y")
    context = {"page": "dashboard", "total_students": 1500, "timestamp": my_datetime}
    is_voucher_created = isVoucherAlreadyCreated(user)
    context["is_voucher_created"] = is_voucher_created
    return render(request, "home/dashboard.html", context)


@djangoAdminNotAllowed
@login_required
def setting(request):
    user = getUser(request.user)
    all_department = Department.objects.filter(organization = user.organization)
    print(all_department)
    context = {
        "page": "settings",
        "all_departments":  all_department,
    }
    return render(request, "home/settings.html", context)

@djangoAdminNotAllowed
@login_required
def update_organization(request):
    user = getUser(request.user)
    organization = user.organization
    if request.method == "POST":
        logo = request.FILES.get("logo")
        Type = request.POST.get("type")
        city = request.POST.get("city")
        fee = request.POST.get("fee")

        if logo:
            organization.logo = logo
        if Type != organization.type:
            organization.type = Type
        if city != organization.city:
            organization.city = city
        if fee != organization.point_fee:
            organization.point_fee = fee
        organization.save()
        messages.success(request, "Information has been updated")
        print(request.POST, request.FILES)

    return redirect("dashboard:settings")


@djangoAdminNotAllowed
@login_required
def add_department(request):
    user = getUser(request.user)
    if request.method == "POST":
        departments = request.POST.get("departments")
        if not departments:
            messages.error(request, "Departments required")
            return redirect("dashboard:settings")
        all_departments = departments.split("\n")
        
        try:
            with transaction.atomic():
                for department in all_departments:
                    each_dept = department.split(",")
                    abbr = each_dept[0]
                    name = each_dept[1]
                    Department.objects.create(
                        abbr=abbr, 
                        name=name, 
                        organization=user.organization)
            messages.success(request, "Departments have been added successfully!")
        except Exception as e:
            messages.error(request, "Incorrect format given in input field")

    return redirect("dashboard:settings")
