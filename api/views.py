from dashboard.models import *
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework import exceptions
from django.urls import resolve
from django.conf import settings
from api.models import *
from api.serializers import *
from api.authentication import RequestAuthentication, ApiResponse
from api.support import beautify_errors
import copy
import json
from rest_framework.views import APIView
from django.db.models import Q

# Create your views here.


def index(request):
    return render(request, "abcc.html")


class StudentApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

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
            student = UserInfo(
                uid=uid,
                user=user,
                status="student",
                organization_id=data.get("organization_id"),
                phone=data.get("phone"),
            )
            if data.get("profile_picture"):
                student.profile_picture = data.get("profile_picture")
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

    def delete(self, request, uid):
        try:
            student = UserInfo.objects.get(uid=uid)
            student.user.delete()
            student.delete()
            self.postSuccess({}, "Student deleted successfully")
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


class DriverApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]

    def __init__(self):
        ApiResponse.__init__(self)

    def post(self, request, uid=None):
        try:
            data = request.data.copy()
            stripe_cust_id = self.create_stripe_user(data)
            data["stripe_cust_id"] = stripe_cust_id
            data["uid"] = uid
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user = UserInfo.objects.get(uid=uid)
                self.add_payment_info(user)
                self.postSuccess({"user": serializer.data}, "User added successfully")
            else:
                self.delete_stripe_user(stripe_cust_id)
                self.postError(beautify_errors(serializer.errors))
        except Exception as e:
            self.postError({"uid": str(e)})
        return Response(self.output_object)

    def get(self, request):
        try:
            print(request)
            phone = request.data["phone"]
            pin = request.data["pin"]
            driver = Driver.objects.get(phone=phone, pin=pin)
            org = driver.organization
            shuttles = Shuttle.objects.filter(organization=org)
            response_data = {
                "driver": DriverSerializer(driver, many=False).data,
                "organization": OrgSerializerShortSerializer(org, many=False).data,
                "shuttles": ShuttleSerializer(shuttles, many=True).data,
            }
            if not shuttles.exists():
                message = None
                self.postWarning({"shuttles": "No shuttles added by admin"})
            else:
                message = "Points fetched successfully"
            self.postSuccess(response_data, None)
        except Exception as e:
            self.postError({"driver": str(e)})
        return Response(self.output_object)

    def patch(self, request, uid=None):
        try:
            user_obj = get_object_or_404(UserInfo, uid=uid)
            self.add_payment_info(user_obj)
            if user_obj.email != request.data["email"]:
                self.postError(
                    {
                        "email": "To avoid problems with future signin, Email cannot be updated"
                    }
                )
                return Response(self.output_object)

            serializer = UserSerializer(user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                self.postSuccess({"user": serializer.data}, "User updated successfully")
            else:
                self.postError(beautify_errors(serializer.errors))
        except Exception as e:
            self.postError({"uid": str(e)})
        return Response(self.output_object)
