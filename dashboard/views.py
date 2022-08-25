from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from dashboard.supporting_func import *
from dashboard.models import *
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

# from .serializers import PointSerializer, DriverSerializer
from django.contrib import messages
from django.shortcuts import get_object_or_404
from random import randint, choice



@login_required
def index(request):
    user = getUser(request.user)
    my_datetime = timezone.now().strftime("%B, %Y")
    context = {"page": "dashboard", "total_students": 1500, "timestamp": my_datetime}
    is_voucher_created = isVoucherAlreadyCreated(user)
    context["is_voucher_created"] = is_voucher_created
    return render(request, "home/dashboard.html", context)
    user = getUser(request.user)
    # return redirect(f"/{status}/{}/")
    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/")
    # return
    # return render(request, "dashboard/index.html")


@login_required
def dashboard(request, org_abbr, status, section=None, section_object_id=None):
    context = {}

    user = getUser(request.user)
    if user and user.organization.abbr == org_abbr and user.status.name == status:
        page = user.status.getPageByUrlName(section, section_object_id)
        if page:
            # print(org_abbr, status, section, section_object_id)
            page_context = page.getPageData(user, section_object_id)
            page_context["current_section"] = section
            print(page_context)
            return render(request, page.template, page_context)
        else:
            return redirect("dashboard:index")
    return redirect("dashboard:index")


@login_required
def particularVoucher(request, org_abbr, voucher_id):
    return render(request, "dashboard/admin/particular_voucher.html")


def getDashboardInfo(request):
    output = extraValidation(request.user)
    user = output["user"]
    output_response = output["parameters"]
    if user and output_response["status"]:
        # Dashboard data for admin
        if user.status.name == "admin":
            output_response["fields"] = {"is_to_create_qr": isToCreateQR(user)}

        # Dashboard data for student
        if user.status.name == "student":
            voucher_to_pay = isVoucherAlreadyCreated(user)
            output_response["fields"] = {
                "voucher": voucher_to_pay.getJson()
                if voucher_to_pay
                else voucher_to_pay
            }

    return JsonResponse(output_response)


# ADMIN specific


def createVoucher(request):
    output = extraValidation(request.user, "admin")
    user = output["user"]
    output_response = output["parameters"]
    if user and output_response["status"]:
        try:
            # Creating new voucher
            new_voucher = Voucher(organization=user.organization, created_by=user)
            new_voucher.setDefaultValues()
            output_response["message"] = "Voucher has been generated successfully!"
        except Exception as e:
            output_response["status"] = False
            output_response["message"] = str(e)

        # Dashboard data for admin
        output_response["fields"] = {"is_to_create_qr": isToCreateQR(user)}

    return JsonResponse(output_response)


# Admin specific


def getVoucherHistory(request):
    output = extraValidation(request.user, "admin")
    user = output["user"]
    output_response = output["parameters"]
    if user and output_response["status"]:
        # Dashboard data for admin
        voucher_history_queryset = Voucher.objects.filter(
            created_by=user, organization=user.organization
        ).order_by("-pk")
        voucher_history_list = list(voucher_history_queryset)
        serialized_qs = serializers.serialize("json", voucher_history_list)
        output_response["fields"] = {"voucher_history": serialized_qs}

    return JsonResponse(output_response)


# Admin specific


# Admin specific
def getStudents(request):
    output = extraValidation(request.user, "admin")
    user = output["user"]
    output_response = output["parameters"]
    if user and output_response["status"]:
        # Dashboard data for admin
        students = UserInfo.objects.filter(organization=user.organization)
        temp_student_list = []
        for student in students:
            if student.status.name == "student":
                temp_student_list.append(student.getJson())
        # serialized_qs = serializers.serialize('json', voucher_history_list)
        output_response["fields"] = {"students": temp_student_list}

    return JsonResponse(output_response)


# def point_del(request):
#   return


# def getPoint(self, request):
#     queryset = Point.objects.all().values()
#     return Response(queryset)

# def editPoint(request):
#     request.POST.get('description')
#     points_list = Point.objects.all()
#     return Response(points_list)


@login_required
def postPoint(request):
    user = getUser(request.user)
    try:
        point_name = request.POST["description"]

        x = Point.objects.create(
            vehicle_name=point_name, organization=user.organization
        )
        messages.success(request, "Point has been added successfully!")

    except Exception as e:
        messages.error(request, str(e))

    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/points")
    else:
        return redirect("index")


@login_required
def update_points(request):
    user = getUser(request.user)

    point_id = request.POST["edit_point_id"]
    point_name = request.POST["edit_point_name"]

    try:
        selected_point = get_object_or_404(Point, pk=point_id)
        selected_point.vehicle_name = point_name
        selected_point.save()
        messages.success(request, "Point has been updated successfully!")

    except Exception as e:
        messages.error(request, str(e))

    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/points")
    else:
        return redirect("index")


@login_required
def delete_point(request):
    user = getUser(request.user)

    point_id = request.POST["point_id_delete"]

    try:
        selected_point = get_object_or_404(Point, pk=point_id)
        selected_point.delete()
        messages.success(request, "Point has been deleted successfully!")

    except Exception as e:
        messages.error(request, str(e))

    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/points")
    else:
        return redirect("index")

    # return render(request,'dashboard/admin/points.html')


@login_required
def addDriver(request):
    user = getUser(request.user)
    try:
        dfname = request.POST["first_name"]
        dlname = request.POST["last_name"]
        dnum = request.POST["d_number"]
        x = Driver.objects.create(
            driver_fname=dfname,
            driver_lname=dlname,
            driver_num=dnum,
            organization=user.organization,
        )
        messages.success(request, "Driver has been added successfully!")

    except Exception as e:
        messages.error(request, str(e))

    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/drivers")
    else:
        return redirect("index")


@login_required
def update_drivers(request):
    user = getUser(request.user)

    driver_id = request.POST["edit_driver_id"]
    dfname = request.POST["fname"]
    dlname = request.POST["lname"]
    dnum = request.POST["d_num"]

    try:
        selected_driver = get_object_or_404(Driver, pk=driver_id)
        selected_driver.driver_fname = dfname
        selected_driver.driver_lname = dlname
        selected_driver.driver_num = dnum
        selected_driver.save()
        messages.success(request, "Driver has been updated successfully!")

    except Exception as e:
        messages.error(request, str(e))

    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/drivers")
    else:
        return redirect("index")


@login_required
def delete_drivers(request):
    user = getUser(request.user)

    driver_id = request.POST["driver_id_delete"]

    try:
        selected_driver = get_object_or_404(Driver, pk=driver_id)
        selected_driver.delete()
        messages.success(request, "Driver has been deleted successfully!")

    except Exception as e:
        messages.error(request, str(e))

    if user:
        return redirect(f"/{user.organization.abbr}/{user.status.name}/drivers")
    else:
        return redirect("index")
