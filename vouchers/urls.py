import imp
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from vouchers.views import *

app_name = "vouchers"
urlpatterns = [
    path("", view=vouchers, name="all"),
    path("<voucher_id>/view", view=single_voucher, name="single_voucher"),
    path("create", view=create_voucher, name="create-voucher"),

]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
