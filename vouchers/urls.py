from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include


app_name = "vouchers"
urlpatterns = [
    path("", view=views.vouchers, name="all"),
    path("<voucher_id>/view", view=views.single_voucher, name="single_voucher"),
    path("create", view=views.create_voucher, name="create-voucher"),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
