from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required


app_name = "shuttles"
urlpatterns = [
    path("", login_required(views.ShuttleDetailView.as_view()), name="all"),
    path(
        "<pk>/view",
        login_required(views.ShuttleDetailView.as_view()),
        name="select-shuttle",
    ),
    # path("", view=views.all_drivers, name="all"),
    # path("<driver_id>/view/", view=views.select_driver, name="select-driver"),
    path("<shuttle_id>/edit/", view=views.edit_shuttle, name="edit-shuttle"),
    path("add/", view=views.add_shuttle, name="add-shuttle"),
    path("<shuttle_id>/delete/", view=views.delete_shuttle, name="delete-shuttle"),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
