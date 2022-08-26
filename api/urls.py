from django.urls import path

from payment.models import Account
from . import views
from api.views import *
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    # path("student", StudentApi.as_view()),
    path("student/<uid>", StudentApi.as_view()),
    path("student", StudentApi.as_view(), name="student"),
    path("", views.index, name="index"),

    path("driver/login", DriverApi.as_view()),
    path("driver/logout", DriverApi.as_view(), name="driver-shuttle"),
    path("driver/shuttle", DriverShuttleApi.as_view(), name="driver-shuttle"),    
    path("organization", OrganizationApi.as_view(), name="organization"),
    path("account", AccountApi.as_view(), name="payment"),

    # Voucher api
    path("voucher/is_available", VoucherApi.as_view(), name="voucher"),

]


urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
