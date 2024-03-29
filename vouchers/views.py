from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.supporting_func import *
from dashboard.models import *
from dashboard.supporting_func import getUser
from django.contrib import messages
from payment.models import FeeSubmission
from vouchers.models import *
from authentication.decorators import djangoAdminNotAllowed

# from rest_framework import generics, status, viewsets
# Create your views here.

@djangoAdminNotAllowed
@login_required
def transactions(request, voucher_id):
    user = getUser(request.user)
    voucher = Voucher.objects.filter(
        id=voucher_id, organization=user.organization
    ).first()
    if not voucher:
        messages.error(
            request, "Voucher doesn't exist with this id OR you don't have access"
        )
        return redirect("vouchers:all")

    fee_submissions = FeeSubmission.objects.filter(voucher = voucher)
    print(fee_submissions)

    context = {
        "fee_submissions": fee_submissions,
        "single_voucher": Voucher.objects.filter(id=voucher_id).first(),
    }
    return render(request, "home/transactions.html", context)



@djangoAdminNotAllowed
@login_required
def create_voucher(request):
    myuser = getUser(request.user)
    is_already_created = isVoucherAlreadyCreated(myuser)
    if is_already_created:
        messages.info(request, "Voucher already created")
        return redirect("vouchers:single_voucher", voucher_id=is_already_created.id)

    if request.method == "POST":
        new_voucher = Voucher(organization=myuser.organization, created_by=myuser)
        new_voucher.setDefaultValues()
        messages.success(
            request, "Voucher has been created successfully, you can print it now!"
        )
        return redirect("vouchers:single_voucher", voucher_id=new_voucher.id)

    my_datetime = timezone.now().strftime("%B, %Y")
    context = {"page": "vouchers", "timestamp": my_datetime}
    return render(request, "home/vouchers/create.html", context)


def getAllVouchers(organization):
    return Voucher.objects.filter(organization=organization)

@djangoAdminNotAllowed
@login_required
def vouchers(request):
    user = getUser(request.user)
    is_already_created = isVoucherAlreadyCreated(user)
    my_datetime = timezone.now().strftime("%B, %Y")
    context = {
        "page": "vouchers",
        "timestamp": my_datetime,
        "is_voucher_created": is_already_created,
        "all_vouchers": getAllVouchers(user.organization),
    }
    return render(request, "home/vouchers/vouchers.html", context)


@djangoAdminNotAllowed
@login_required
def single_voucher(request, voucher_id):
    user = getUser(request.user)
    is_already_created = isVoucherAlreadyCreated(user)
    my_datetime = timezone.now().strftime("%B, %Y")
    context = {
        "page": "vouchers",
        "timestamp": my_datetime,
        "is_voucher_created": is_already_created,
        "all_vouchers": getAllVouchers(user.organization),
    }
    # my voucher
    voucher = Voucher.objects.filter(
        id=voucher_id, organization=user.organization
    ).first()
    if voucher:
        context["single_voucher"] = voucher
    else:
        messages.error(
            request, "Voucher doesn't exist with this id OR you don't have access"
        )
        return redirect("vouchers:all")
    return render(request, "home/vouchers/vouchers.html", context)




