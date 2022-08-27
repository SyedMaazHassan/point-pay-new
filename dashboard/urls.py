from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from dashboard import views
from django.urls import path, include


app_name = "dashboard"
urlpatterns = [
    path("", view=views.index, name="index")
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
