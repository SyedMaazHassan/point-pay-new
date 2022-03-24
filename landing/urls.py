from django.urls import path
from . import views

app_name = "landing"
urlpatterns = [
    path("", view=views.index, name="index")
]
