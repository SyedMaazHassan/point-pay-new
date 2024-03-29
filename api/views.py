from urllib import request
from dashboard.models import *
from dashboard.supporting_func import getUserByUid, isVoucherAlreadyCreated
from payment.models import Account, FeeSubmission
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework import exceptions
from django.urls import resolve
from django.conf import settings
from api.models import *
from api.serializers import *
from api.authentication import RequestAuthentication, ApiResponse
from api.support import beautify_errors
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from payment.models import Account
import stripe
stripe.api_key = settings.STRIPE['secretKey']
# Create your views here.


def index(request):
    return render(request, "dashboard/abc.html")


class AccountApi(APIView, ApiResponse):
    def __init__(self):
        ApiResponse.__init__(self)

    def get(self, request):
        try:
            uid = request.headers.get("uid")        
            user = getUserByUid(uid)
            account = Account.objects.filter(user = user).first()
            if not account:
                raise Exception("Account not found")
            serialized_account = AccountSerializer(account, many = False).data
            output = {
                "account": serialized_account
            }
            self.postSuccess(output, "Account fetched successfully")
        except Exception as e:
            self.postError({"account": str(e)})
        return Response(self.output_object)


class StudentApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def create_stripe_user(self, first_name, last_name, email):
        full_name = f"{first_name} {last_name}"
        customer = stripe.Customer.create(
            name = full_name,
            email = email
        )
        return customer['id']

    def createStudent(self, data, uid):
        all_students = UserInfo.objects.all()
        if data.get("phone"):
            if all_students.filter(phone=data.get("phone")).exists():
                raise Exception("Student with this phone number already exists!")
        if all_students.filter(uid=uid).exists():
            raise Exception("Student with this UID already exists!")
        # Step 1 - Create django user
        user = User.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("email"),
            email=data.get("email"),
            password=data.get("password"),
        )
        # Step 2 - Create UserInfo Object with status = 'student'
        try:
            roll_no = data.get("roll_no")
            if not roll_no:
                raise Exception("Roll no. is required.")
            profile_picture = data.get("profile_picture")
            id_card_front_pic = data.get("id_card_front_pic")
            id_card_back_pic = data.get("id_card_back_pic")
            student = UserInfo(
                uid=uid,
                user=user,
                status="student",
                roll_no=roll_no,
                organization_id=data.get("organization_id"),
                phone=data.get("phone")
            )
            if id_card_front_pic and id_card_back_pic:
                student.id_card_front_pic = id_card_front_pic
                student.id_card_back_pic = id_card_back_pic
            
            if profile_picture:
                student.profile_picture = profile_picture
            student.save()
            stripe_cust_id = self.create_stripe_user(user.first_name, user.last_name, user.username)
            student.stripe_cust_id = stripe_cust_id
            student.save()
            return student
        except Exception as e:
            user.delete()
            raise Exception(str(e))

    def post(self, request, uid=None):
        try:
            if not uid:
                raise Exception("UID is required to create student")
            data = request.data
            student = self.createStudent(data, uid)
            serialized_student = UserSerializer(student, many=False)
            self.postSuccess(
                {"student": serialized_student.data}, "Student registered successfully"
            )
        except Exception as e:
            self.postError({"student": str(e)})
        return Response(self.output_object)

    def get(self, request, uid=None):
        try:
            output = {}
            if not uid:
                user_object = UserInfo.objects.all()
                many = True
            else:
                user_object = get_object_or_404(UserInfo, uid=uid)
                many = False
            print(uid)
            serializer = UserSerializer(user_object, many=many)
            output["student"] = serializer.data
            self.postSuccess(output, "Student fetched successfully")
        except Exception as e:
            self.postError({"student": str(e)})
        return Response(self.output_object)


    def patch(self, request, uid):
        try:
            data = request.data
            student = UserInfo.objects.get(uid=uid)
            if data.get("phone"):
                student.phone = data.get("phone")
            if data.get("profile_picture"):
                student.profile_picture = data.get("profile_picture")
            if data.get("roll_no"):
                student.roll_no = data.get("roll_no")
            student.save()
            if request.data.get("email") and student.user.email != request.data.get(
                "email"
            ):
                raise Exception("Email address can't be updated")
            if request.data.get("organization_id") and student.organization.id != int(
                request.data.get("organization_id")
            ):
                raise Exception(f"{student.organization.type} can't be updated")

            user = student.user
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")
            user.save()

            output = {}
            serialized_student = UserSerializer(student, many=False)
            output["student"] = serialized_student.data
            self.postSuccess(output, "Student updated successfully")
        except Exception as e:
            self.postError({"student": str(e)})
        return Response(self.output_object)


from drivers.models import *
from shuttles.models import *
from dashboard.models import Organization


class OrganizationApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def get(self, request):
        try:
            orgs = Organization.objects.all()
            response_data = {
                "organization": OrgSerializerShortSerializer(orgs, many=True).data,
            }
            self.postSuccess(response_data, None)
        except Exception as e:
            self.postError({"organization": str(e)})
        return Response(self.output_object)




class DriverShuttleApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)


    def get(self, request):
        try:
            session_id = request.headers.get("session_id")
            driver_session = DriverSession.objects.get(session_id = session_id)
            shuttles = Shuttle.objects.filter(
                organization = driver_session.driver.organization
            )
            response_data = {
                "shuttle": ShuttleSerializer(shuttles, many=True).data,
            }
            if not shuttles.exists():
                message = None
                self.postWarning({"shuttles": "No shuttles added by admin"})
            else:
                message = "Shuttles fetched successfully"
            self.postSuccess(response_data, None)
        except Exception as e:
            self.postError({"shuttle": str(e)})
        return Response(self.output_object)

    def patch(self, request, uid=None):
        try:
            message = ""

            session_id = request.headers.get("session_id")
            driver_session = DriverSession.objects.get(session_id = session_id)
 
            driver = driver_session.driver
            to_do = request.data.get("to_do")
            shuttle_id = request.data.get("shuttle_id")
            shuttle = Shuttle.objects.get(shuttle_id = shuttle_id)

            # Check if shuttle and driver belong to same org
            if shuttle.organization_id != driver.organization_id:
                raise Exception("Invalid shuttle id")

            if to_do not in ["start", "stop"]:
                raise Exception("Invalid operation to perform")

            if to_do == "start":
                if shuttle.is_running:
                    raise Exception("Shuttle is already being driven. Select another")
                shuttle.is_running = True
                shuttle.save()
                message = "Shuttle has been started successfully"

            if to_do == "stop":
                if not shuttle.is_running:
                    raise Exception("Shuttle is already stopped")
                shuttle.is_running = False
                shuttle.save()
                message = "Shuttle has been stopped successfully"


            serializer = ShuttleSerializer(shuttle, many=False)
            self.postSuccess({"shuttle": serializer.data}, message)

        except Exception as e:
            self.postError({"shuttle": str(e)})

        return Response(self.output_object)



# To login and logout the driver
class DriverApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)


    def post(self, request):
        try:
            phone = request.data.get("phone")
            pin = request.data.get("pin")

            if not phone:
                raise Exception("Phone no. is required")

            if not pin:
                raise Exception("PIN is required")
            
            phone = phone.replace(" ", "+")
            
            driver = Driver.objects.filter(phone=phone, pin=pin).first()
            if not driver:
                raise Exception("Invalid driver credentials")
            
            
            # Creating driver session
            new_driver_session = DriverSession(
                driver = driver
            )
            new_driver_session.save()

            # serialized driver session
            serialized_session = DriverSessionSerializer(new_driver_session, many = False).data

            response_data = {
                "session": serialized_session,
            }        
            self.postSuccess(response_data, "Driver is logged in successfully")

        except Exception as e:
            self.postError({"driver": str(e)})
        return Response(self.output_object)

    def patch(self, request):
        try:
            session_id = request.headers.get("session_id")
            driver_session = DriverSession.objects.get(session_id = session_id)
            driver_session.delete()            
            self.postSuccess({}, "Driver logged out successfully!")
        except Exception as e:
            self.postError({"uid": str(e)})
        return Response(self.output_object)


# voucher api
class VoucherApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def get(self, request):
        try:
            uid = request.headers.get("uid")        
            user = getUserByUid(uid)
            voucher_created = isVoucherAlreadyCreated(user)

            if voucher_created:
                fee_submission_obj = FeeSubmission.objects.filter(
                    user = user, 
                    voucher = voucher_created
                ).first()
                if fee_submission_obj:
                    voucher_created = None

            response = {
                "voucher": {
                    "is_available": voucher_created != None,
                    "created_since": voucher_created.created_at if voucher_created else None
                }
            }
            self.postSuccess(response, None)
        except Exception as e:
            self.postError({"voucher": str(e)})
        return Response(self.output_object)