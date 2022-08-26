from dashboard.supporting_func import getUser

def current_user(request):
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