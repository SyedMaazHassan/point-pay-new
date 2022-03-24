from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required

app_name = "drivers"
urlpatterns = [
    path("", login_required(views.DriverDetailView.as_view()), name="all"),
    path(
        "<pk>/view",
        login_required(views.DriverDetailView.as_view()),
        name="select-driver",
    ),
    # path("", view=views.all_drivers, name="all"),
    # path("<driver_id>/view/", view=views.select_driver, name="select-driver"),
    path("<driver_id>/edit/", view=views.edit_driver, name="edit-driver"),
    path("add/", view=views.add_driver, name="add-driver"),
    path("<driver_id>/delete/", view=views.delete_driver, name="delete-driver"),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
