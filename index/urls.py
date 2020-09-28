from django.urls import path
from . import views
from .views import AllUsers

urlpatterns = [
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('edit-user/', views.update_person, name='edit_user'),
    path('all-users/', AllUsers.as_view(), name='all_users'),

    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),

]
