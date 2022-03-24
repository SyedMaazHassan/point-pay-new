# from dashboard.models import *
# def userStatus(user):
#     status_dictionary = {
#         "status": None,
#         "user": user
#     }
#     admin_check = OrgAdmin.objects.filter(user=user)
#     if admin_check.exists():
#         admin_user = admin_check[0]
#         status_dictionary["status"] = "admin"
#         status_dictionary["user"] = admin_user
#     return status_dictionary

from os import stat
from dashboard.models import Organization, UserInfo, Voucher
from django.utils import timezone
from datetime import datetime


def getUser(user):
    user_info_query = UserInfo.objects.filter(user=user)
    if user_info_query.exists():
        user_info_object = user_info_query[0]
        return user_info_object
    return None


def isVoucherAlreadyCreated(user):
    current_date = timezone.now()
    print(current_date.month, current_date.year)
    check_voucher_query = Voucher.objects.filter(
        organization=user.organization,
        month=current_date.month,
        year=current_date.year
    ).order_by("-created_at")
    print(check_voucher_query)
    if check_voucher_query.exists():
        # returning last recent voucher
        return check_voucher_query[0]
    else:
        return False


def isToCreateQR(user):
    current_date = timezone.now()
    status = isVoucherAlreadyCreated(user)
    if status:
        qr_code_info = status.getJson()
        output = {
            "status": False,
            "info": {
                "button": {
                    "icon": "fa-download",
                    "text": "Download QR code"
                },
                "popup_title": "Download QR code",
            } | qr_code_info
        }
    else:
        output = {
            "status": True,
            "info": {
                "button": {
                    "icon": "fa-plus",
                    "text": "Create QR code"
                },
                "popup_title": "Create Voucher",
                "month": current_date.strftime("%b"),
                "year": current_date.year,
                "price": f"Rs. {round(user.organization.point_fee, 0)}"
            }
        }

    return output


def extraValidation(default_user_object, scope=None):
    output = {
        "user": None,
        "parameters": {
            "fields": {}
        }
    }
    if default_user_object.is_authenticated:
        user = getUser(default_user_object)
        # Check if user exists
        if user:
            if (scope and user.status.name == scope) or (scope is None):
                output["parameters"]["status"] = True
                output["parameters"]["message"] = ""
                output["user"] = user
            else:
                output["parameters"]["status"] = False
                output["parameters"]["message"] = "You don't have access for this operation!"
        else:
            output["parameters"]["status"] = False
            output["parameters"]["message"] = "User external profile not found!"
    else:
        output["parameters"]["status"] = False
        output["parameters"]["message"] = "Authentication required, user is not logged in!"

    return output
