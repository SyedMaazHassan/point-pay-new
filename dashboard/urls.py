from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from dashboard import views
from django.urls import path, include


app_name = "dashboard"
urlpatterns = [
    path("", view=views.index, name="index"),
    path("<voucher_id>/transactions", view=views.transactions, name="transactions"),
    # path("vouchers", view=views.vouchers, name="vouchers"),
    # path("<org_abbr>/<status>/",
    #      view=views.dashboard, name="dashboard"),
    # path("<org_abbr>/<status>/<section>/",
    #      view=views.dashboard, name="dashboard"),
    # path("<org_abbr>/<status>/<section>/<section_object_id>/",
    #      view=views.dashboard, name="dashboard"),
    # # path("<org_abbr>/admin/vouchers/<voucher_id>/",
    # #      view=views.particularVoucher, name="voucher"),
    # path(
    #     "get_dashboard_info",
    #     view=views.getDashboardInfo,
    #     name="get_dashboard_info"
    # ),
    # path(
    #     "create_voucher",
    #     view=views.createVoucher,
    #     name="create_voucher"
    # ),
    # path(
    #     "get_voucher_history",
    #     view=views.getVoucherHistory,
    #     name="get_voucher_history"
    # ),
    # path(
    #     "get_students",
    #     view=views.getStudents,
    #     name="get_students"
    # ),
    # path(
    #     "postPoint",
    #     view=views.postPoint,
    #     name="postPoint"
    #  ),
    # path(
    #     "update_points",
    #     view=views.update_points,
    #     name="update_points"
    #  ),
    #  path(
    #     "delete_point",
    #     view=views.delete_point,
    #     name="delete_point"
    #  ),
    #  path(
    #     "addDriver",
    #     view=views.addDriver,
    #     name="addDriver"
    #  ),
    #  path(
    #     "update_drivers",
    #     view=views.update_drivers,
    #     name="update_drivers"
    #  ),
    #  path(
    #     "delete_drivers",
    #     view=views.delete_drivers,
    #     name="delete_drivers"
    #  )
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
