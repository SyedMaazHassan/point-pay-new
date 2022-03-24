from dashboard.supporting_func import getUser

def current_user(request):
    user = getUser(request.user) if request.user.is_authenticated else None
    return { 'myuser': user}