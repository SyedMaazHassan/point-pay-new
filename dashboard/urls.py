from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from dashboard import views
from django.urls import path, include


app_name = "dashboard"
urlpatterns = [
    path("", view=views.index, name="index"),
    path("settings/", view=views.setting, name="settings"),
    path("update-organization/", view=views.update_organization, name="update-organization"),
    path("add-department/", view=views.add_department, name="add-department"),
    
    
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
