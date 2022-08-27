from django.urls import path
from payment.views import *
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [

    path("api/payment/initiate", PaymentApi.as_view(), name="payment"),
    path("api/payment/verify", PaymentApi.as_view(), name="payment"),
    path("api/payment/history", PaymentHistoryApi.as_view(), name="payment"),
    path("wallet/", wallet, name="wallet"),
    path("withdraw/", withdraw_funds, name="withdraw")

]


urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
