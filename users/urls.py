from django.contrib.auth import views as auth_views
from django.urls import path
from .views import SuperuserSignupView
from allauth.account import views as allauth_views
from . import views

urlpatterns = [
    path('signup/', SuperuserSignupView.as_view(), name='account_signup'),
    path('login/', allauth_views.LoginView.as_view(), name='account_login'),
    path('logout/', allauth_views.LogoutView.as_view(), name='account_logout'),

    path('password/change/', allauth_views.PasswordChangeView.as_view(), name='account_change_password'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='account_change_password_done'),
    path('password/reset/', allauth_views.PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),

    path('management/', views.user_management, name='user_management'),
    path('toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),

    path('profile/<int:user_id>/', views.view_profile, name='the_user_profile'),
]
