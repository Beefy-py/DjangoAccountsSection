from django.urls import path
from django.conf import settings
from .views import BlogListView, PostCreateView, PostDeleteView, PostDetailView, PostUpdateView


urlpatterns = [
    path('', BlogListView.as_view(), name='post_list'),
    path('detail-post/<str:pk>/', PostDetailView.as_view(), name='detail_post'),
    path('update-post/<str:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('delete-post/<str:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('create-post/', PostCreateView.as_view(), name='create_post')
]
