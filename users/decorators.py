from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

# def teacher_or_admin_required(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         user = request.user

#         if not user.is_authenticated:
#             return redirect('login')  
        

#         if user.is_staff or user.is_superuser:
#             return view_func(request, *args, **kwargs)

#         if hasattr(user, 'user_type') and user.user_type.user_type == 'teacher':
#             return view_func(request, *args, **kwargs)

#         raise PermissionDenied("You are not allowed to access this page.")

#     return _wrapped_view

def teacher_or_admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        if user.is_staff or user.is_superuser:
            return view_func(request, *args, **kwargs)

        if hasattr(user, 'teacherprofile_profile'):
            return view_func(request, *args, **kwargs)

        raise PermissionDenied("You are not allowed to access this page.")

    return _wrapped_view
