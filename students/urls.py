from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include


app_name = "students"
urlpatterns = [
    path("", view=views.students, name="all"),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
