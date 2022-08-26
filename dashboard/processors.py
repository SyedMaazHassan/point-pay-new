from dashboard.supporting_func import getUser
from django.shortcuts import redirect

def current_user(request):
    if request.user.is_superuser:
        return redirect("/admin")


    user = getUser(request.user) if request.user.is_authenticated else None
    return { 'myuser': user}


def current_base_domain(request):
    from django.conf import settings
    enviro = settings.ENVIRO
    if enviro == "local":
        domain = f"http://{settings.LOCALHOST}/"
    elif enviro == "live":
        domain = f"http://{settings.LIVEHOST}/"
    else:
        raise Exception("Unknown environment")

    print(enviro, domain)
    return {"domain": domain}