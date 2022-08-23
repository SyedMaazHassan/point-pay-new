from django.urls import path
from payment.views import *
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [

    path("payment/initiate", PaymentApi.as_view(), name="payment"),
    path("payment/verify", PaymentApi.as_view(), name="payment"),
    


    # path("student", StudentApi.as_view()),
    # path("student/<uid>", StudentApi.as_view(), name="student"),
    # path("", views.index, name="index"),

    # path("driver/login", DriverApi.as_view()),
    # path("driver/logout", DriverApi.as_view(), name="driver-shuttle"),
    # path("driver/shuttle", DriverShuttleApi.as_view(), name="driver-shuttle"),    
    # path("organization", OrganizationApi.as_view(), name="organization"),


    # # Voucher api
    # path("voucher/is_available", VoucherApi.as_view(), name="voucher"),
]


urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
