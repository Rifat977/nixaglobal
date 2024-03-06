from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('core:index')
    return _wrapped_view

def agent_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_agent or request.user.is_exclusive_agent):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('core:index')
    return _wrapped_view

def sub_agent_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_sub_agent:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('core:index')
    return _wrapped_view

def exclusive_agent_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_exclusive_agent:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('core:index')
    return _wrapped_view


def any_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and (user.is_admin or user.is_agent or user.is_sub_agent or user.is_exclusive_agent):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('core:index')
    return _wrapped_view