from django.shortcuts import render
from allauth.account.views import SignupView
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from allauth.account.forms import SignupForm
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
# from .models import CustomUser
from django.contrib.auth.models import User




class SuperuserSignupView(UserPassesTestMixin, FormView):
    template_name = "account/signup.html"
    form_class = SignupForm
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("Only superusers can create accounts.")
        else:
            return redirect('admin:login')
    
    def form_valid(self, form):
        user = form.save(self.request)
        
        messages.success(
            self.request, 
            f"Account created successfully for {user.username}. The user can now log in."
        )
        
        return redirect('admin:auth_user_changelist')



def superuser_required(view_func):
    """Decorator to ensure user is superuser"""
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/admin/login/'
    )(view_func)
    return decorated_view_func


@superuser_required
def user_management(request):
    # Get all users with related profiles - FIXED related_names
    users = User.objects.all().select_related('studentprofile_profile', 'teacherprofile_profile')
    
    
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(studentprofile_profile__student_id__icontains=search_query) |
            Q(teacherprofile_profile__employee_id__icontains=search_query)
        )
    
    # Filter by user type - USING PROFILE EXISTENCE (Option 2)
    user_type = request.GET.get('user_type', '')
    if user_type == 'student':
        users = users.filter(studentprofile_profile__isnull=False)
    elif user_type == 'teacher':
        users = users.filter(teacherprofile_profile__isnull=False)
    elif user_type == 'no_profile':
        users = users.filter(
            studentprofile_profile__isnull=True,
            teacherprofile_profile__isnull=True
        )

    # Filter by active status
    is_active = request.GET.get('is_active', '')
    if is_active == 'active':
        users = users.filter(is_active=True)
    elif is_active == 'inactive':
        users = users.filter(is_active=False)
    
    # Sort functionality
    sort_by = request.GET.get('sort', '-date_joined')
    if sort_by in ['username', 'email', 'date_joined', 'last_login']:
        users = users.order_by(sort_by)
    else:
        users = users.order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
        'selected_user_type': user_type,
        'selected_status': is_active,
        'sort_by': sort_by,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'inactive_users': users.filter(is_active=False).count(),
    }
    
    return render(request, 'users/user_management.html', context)

@superuser_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    action = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User {user.username} has been {action}.")
    
    return redirect('user_management')

