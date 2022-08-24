from dashboard.models import *
from dashboard.supporting_func import getUserByUid, getVoucherByCode, getAccountByOrg, getAccountByUser
from payment.models import *
from rest_framework.response import Response
from api.serializers import *
from api.authentication import RequestAuthentication, ApiResponse
from api.support import beautify_errors
from rest_framework.views import APIView
from django.db.models import Q
from api.serializers import VoucherSerializer
from payment.serializers import *
# Create your views here.



# Payment api
class PaymentApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def validateSignature(self, signature, user):
        request_confirmation_obj = RequestConfirmation.objects.filter(
            signature = signature,
            user = user
        ).first()
        if not request_confirmation_obj:
            raise Exception("Signature is invalid")
        if request_confirmation_obj.is_expired():
            raise Exception("Payment session has been expired. Scan the QR code again.")
        if request_confirmation_obj.is_used:
            raise Exception("Payment session has been expired. Scan the QR code again")
        request_confirmation_obj.is_used = True
        request_confirmation_obj.save()
        return request_confirmation_obj

    def validateVoucher(self, voucher, user):
        is_already_paid = FeeSubmission.objects.filter(
            voucher = voucher,
            user = user
        ).exists()
        if is_already_paid:
            raise Exception("Voucher has already been paid")
        if voucher.is_expired:
            raise Exception("Voucher has been expired")
        return True
    
    def getSerializedVoucher(self, voucher):
        return VoucherSerializer(voucher, many=False).data

    def getSerializedCard(self, fee_submission):
        return FeeSubmissionSerializer(fee_submission, many=False).data

    def get(self, request):
        try:
            code = request.query_params.get("code")
            user = getUserByUid(request.headers.get("uid"))
            voucher = getVoucherByCode(code, user)
            self.validateVoucher(voucher, user)
            

            request_confirmation_obj = RequestConfirmation.objects.create(
                user = user,
                voucher = voucher
            )

            organization = voucher.organization

            # voucher_created = isVoucherAlreadyCreated(user)
            response = {
                "voucher": self.getSerializedVoucher(voucher),
                "voucher_payment": {
                    "from": {
                        "avatar": user.profile_picture.url,
                        "name": user.user.first_name
                    },
                    "to": {
                        "avatar": organization.logo.url,
                        "name": organization.abbr
                    },
                    "signature": request_confirmation_obj.signature,
                    "availability": "Valid for next 4 minutes"
                }
            }
            self.postSuccess(response, "Payment initiated successfully")
        except Exception as e:
            self.postError({"voucher_payment": str(e)})
        return Response(self.output_object)


    def post(self, request):
        try:
            from django.conf import settings
            point_pay_fee = settings.POINTPAY_FEE
            signature = request.data.get("signature")
            user = getUserByUid(request.headers.get("uid"))
            confirmation_obj = self.validateSignature(signature, user)

            user_account = getAccountByUser(user)
            org_account = getAccountByOrg(user.organization)
            # point_pay_account = getHostAccount()

            with transaction.atomic():
                voucher_fee = confirmation_obj.voucher.price
                amount_to_debit = voucher_fee + point_pay_fee
                # Debit from user account
                transaction1 = user_account.debit(amount_to_debit, "PointPay-wallet", "Fee amount paid to the organization/Institute")
                transaction2 = org_account.credit(voucher_fee, "PointPay-wallet", "Fee amount received from user/student")
                # transaction3 = point_pay_account
                
                fee_submission_obj = FeeSubmission.objects.create(
                    voucher = confirmation_obj.voucher,
                    user = confirmation_obj.user
                )

                transaction1.fee_submission = fee_submission_obj
                transaction1.save()
                transaction2.fee_submission = fee_submission_obj
                transaction2.save()
        
            response = {
                "fee_submission": self.getSerializedCard(fee_submission_obj),
            }
            # expire the signature after using once
            confirmation_obj.is_used = True
            confirmation_obj.save()

            self.postSuccess(response, "Payment completed successfully")
        except Exception as e:
            self.postError({"voucher_payment": str(e)})
        return Response(self.output_object)