from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func

def finance_head_only(view_func):
    @login_required(login_url='login')
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.profile.username == "finance_head":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func