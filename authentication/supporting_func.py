from dashboard.supporting_func import getUser
from django.utils import timezone
from dashboard.models import Voucher


def formIsValid(request, list_of_parameters):
    status = True
    message = ""
    for parameter in list_of_parameters:
        if parameter in request.POST and request.POST.get(parameter):
            temp_status = True
        else:
            temp_status = False
            message += f'{parameter}, '
        status = status and temp_status
    return {
        'status': status,
        'message': f'Please enter <b>{message}</b> before submission!'
    }


def expireVouchers(user):
    # Making the vouchers expired
    user_object = getUser(user)
    all_vouchers = Voucher.objects.filter(
        organization=user_object.organization)
    for voucher in all_vouchers:
        voucher.expireIt()
