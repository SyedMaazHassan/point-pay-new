from os import name
from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path("", view=views.index, name="index"),
    path("register/", view=views.register, name="register"),
    path("login/", view=views.login, name="login"),
    path("login-submit/", view=views.login_submit, name="login-submit"),
    path("logout/", view=views.logout, name="logout"),
]


