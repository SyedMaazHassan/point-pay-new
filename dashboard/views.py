from django.contrib.auth.decorators import login_required
from dashboard.supporting_func import *
from dashboard.models import *
from django.shortcuts import render
from authentication.decorators import djangoAdminNotAllowed

@djangoAdminNotAllowed
@login_required
def index(request):
    user = getUser(request.user)
    my_datetime = timezone.now().strftime("%B, %Y")
    context = {"page": "dashboard", "total_students": 1500, "timestamp": my_datetime}
    is_voucher_created = isVoucherAlreadyCreated(user)
    context["is_voucher_created"] = is_voucher_created
    return render(request, "home/dashboard.html", context)