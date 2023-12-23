# create a decorator to check if the user is superuser or not

from django.shortcuts import redirect
from django.http import HttpResponse


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func