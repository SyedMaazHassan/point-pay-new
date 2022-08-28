from calendar import c
import re
from django.contrib import messages
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
from dashboard.supporting_func import getUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from authentication.decorators import djangoAdminNotAllowed
from django.db.models import Sum
import stripe
stripe.api_key = settings.STRIPE['secretKey']

# Create your views here.

@djangoAdminNotAllowed
@login_required
def withdraw_funds(request):
    if request.method == "POST":
        try:
            user = getUser(request.user)
            amount_to_withdraw = request.POST.get("amount_to_withdraw")
            if not amount_to_withdraw:
                messages.error(request, "Amount required to withdraw")
            amount_to_withdraw = float(amount_to_withdraw)
            account = Account.objects.filter(organization = user.organization).first()
            message = "Amount transferred to given bank"
            account.debit(
                amount_to_withdraw,
                "PointPay-wallet",
                message
            )
            messages.success(request, message)
        except Exception as e:
            messages.error(request, str(e))
        
    return redirect("wallet") 


@djangoAdminNotAllowed
@login_required
def wallet(request):
    user = getUser(request.user)
    account = Account.objects.filter(organization = user.organization).first()
    if not account:
        return redirect("dashboard:index")


    all_transaction = Transaction.objects.filter(account = account)
    balance = account.balance_num()
    net_income = FeeSubmission.objects.filter(voucher__organization = user.organization).aggregate(Sum("voucher__price"))
    net_income = net_income["voucher__price__sum"]
    balance = balance if balance else 0
    net_income = net_income if net_income else 0
    withdrawn_funds = net_income - balance

    my_datetime = timezone.now().strftime("%B, %Y")
    context = {
        "page": "transactions",
        "timestamp": my_datetime,
        "all_transactions": all_transaction,
        "balance": balance,
        "withdrawn_funds": withdrawn_funds,
        "net_income": net_income
    }
    return render(request, "home/payment/wallet.html", context)



class PaymentHistoryApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def get(self, request):
        try:
            user = getUserByUid(request.headers.get("uid"))
            transactions = Transaction.objects.filter(account__user = user)
            serialized_transactions = TransactionSerializer(transactions, many = True).data
            print(serialized_transactions)    


            # # voucher_created = isVoucherAlreadyCreated(user)
            response = {
                "payment_history": serialized_transactions
            }
            self.postSuccess(response, "History fetched successfully")
        except Exception as e:
            self.postError({"payment_history": str(e)})
        return Response(self.output_object)



class TopupApi(APIView, ApiResponse):

    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def create_ephemeral_key(self, stripe_cust_id):
        ephemeralKey = stripe.EphemeralKey.create(
            customer=stripe_cust_id,
            stripe_version="2020-03-02"
        )
        return ephemeralKey.secret

    def create_payment_intent(self, stripe_cust_id, amount):
        # amount_in_rs = amount
        # amount_in_dollar = amount_in_rs / 221
        paymentIntent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency="PKR",
            customer=stripe_cust_id,
            automatic_payment_methods={
                'enabled': True,
            }
        )
        return paymentIntent.client_secret


    def get(self, request):
        try:
            # Get subscription
            amount = request.query_params.get("amount")
            if not amount:
                raise Exception("Amount is required")
            amount = int(amount)
            # Get user object
            user = UserInfo.objects.get(uid = request.headers['uid'])
            # Get customer_id
            stripe_cust_id = user.stripe_cust_id
            # Get ephemeralKey 
            ephemeral_key = self.create_ephemeral_key(stripe_cust_id)
            # Get payment Intent
            payment_intent = self.create_payment_intent(stripe_cust_id, amount)
            
            # Create new payment
            # new_payment = Payment(
            #     subscription = subscription,
            #     user = user,
            #     ephemeral_key = ephemeral_key,
            #     payment_intent = payment_intent
            # )
            # new_payment.save()

            output = {
                'payment_sheet': {
                    'paymentIntent': payment_intent,
                    'ephemeralKey': ephemeral_key,
                    'customer': stripe_cust_id,
                    'publishableKey': settings.STRIPE['publishableKey']
                }
            }

            self.postSuccess(output, 'Sheet info collected successfully')
        except Exception as e:
            self.postError({ 'payment_sheet': str(e) })

        return Response(self.output_object)


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