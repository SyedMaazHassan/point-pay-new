from api.models import *
from dashboard.models import UserInfo
from drivers.models import DriverSession
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework import exceptions
import copy
from django.urls import resolve


class ApiResponse:
    def __init__(self):

        self.output_object = {
            "status": 404,
            "success": {"data": None, "message": None},
            "errors": None,
            "warnings": None,
        }

    def postSuccess(self, data, message):
        self.output_object["status"] = 200
        self.output_object["success"]["data"] = data
        self.output_object["success"]["message"] = message

    def postError(self, error_object):
        self.output_object["status"] = 404
        self.output_object["errors"] = error_object


class RequestAuthentication(BaseAuthentication, ApiResponse):
    def __init__(self):
        self.uid_auth_list = ["voucher", "student", "payment"]
        self.session_auth_list = ["driver-shuttle"]

        self.user_auth_list = ["pool.views.UserApi"]
        ApiResponse.__init__(self)

    def authenticateApiKey(self, request):
        status = False
        message = None
        if "api_key" not in request.headers:
            message = "API key is missing"
            return (status, message)
        try:
            API_Key.objects.get(key=request.headers["api_key"])
            status = True
        except API_Key.DoesNotExist:
            message = "Given api key is not valid or it has expired"
        except Exception as e:
            message = str(e).replace("['", "").replace("']", "")
        return (status, {"api_key": message})

    def authenticateUid(self, request):
        status = False
        message = None
        if "uid" not in request.headers:
            message = "Student credentials not provided in headers"
            return (status, message)
        try:
            user = UserInfo.objects.get(uid=request.headers["uid"])
            status = True
        except UserInfo.DoesNotExist:
            message = "Student with given UID does not exist"
        except Exception as e:
            message = str(e).replace("['", "").replace("']", "")
        return (status, {"uid": message})

    def authenticateDriverSession(self, request):
        status = False
        message = None
        if "session_id" not in request.headers:
            message = "Session id is not provided in headers"
            return (status, message)
        try:
            driver_session = DriverSession.objects.get(session_id=request.headers["session_id"])
            status = True
        except DriverSession.DoesNotExist:
            message = "Driver session with given id does not exist, login required."
        except Exception as e:
            message = str(e).replace("['", "").replace("']", "")
        return (status, {"driver": message})

    def authenticate(self, request):
        api_check = self.authenticateApiKey(request)
        if not api_check[0]:
            self.postError(api_check[1])
            raise exceptions.AuthenticationFailed(self.output_object)

        url_name = resolve(request.path_info).url_name
    
        if url_name in self.session_auth_list:
            driver_session_check = self.authenticateDriverSession(request)
            if not driver_session_check[0]:
                self.postError(driver_session_check[1])
                raise exceptions.AuthenticationFailed(self.output_object)

        if url_name in self.uid_auth_list:
            user_check = self.authenticateUid(request)
            if not user_check[0]:
                self.postError(user_check[1])
                raise exceptions.AuthenticationFailed(self.output_object)

        return (True, None)
