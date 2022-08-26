from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import get_messages
from authentication.supporting_func import *
from authentication.forms import *
from authentication.decorators import djangoAdminNotAllowed
# Create your views here.


def index(request):
    return redirect("authentication:login")


def error_404_handler(request, exception):
    return render(request, 'home/page-404.html')

def login(request):
    print("abc")
    context = {
        'form': LoginForm()
    }
    return render(request, "accounts/login.html", context)


def login_submit(request):
    if request.method == "POST":
        form_check = formIsValid(request, ["username", "password"])
        if form_check['status']:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and not user.is_superuser:
                auth.login(request, user)
                print(user)

                # Expire vouchers
                expireVouchers(user)

                return redirect("dashboard:index")
            else:
                messages.error(request, "Username or password is incorrect!")
        else:
            messages.error(request, form_check['message'])

    return redirect("authentication:login")


def logout(request):
    auth.logout(request)
    return redirect("authentication:login")
