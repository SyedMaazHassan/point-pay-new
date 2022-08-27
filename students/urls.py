from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include


app_name = "students"
urlpatterns = [
    path("", view=views.students, name="all"),
    path("<student_id>/view/", view=views.students, name="view-student"),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
