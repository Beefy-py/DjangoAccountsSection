from django.urls import path
from . import views
from .views import AllUsers
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('edit-user/', views.update_person, name='edit_user'),
    path('all', AllUsers.as_view(), name='all_users'),

    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='index/password_reset.html'),
         name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='index/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='index/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='index/password_reset_complete.html'),
         name='password_reset_complete'),

]
