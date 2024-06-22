from django.urls import path
from .views import home, BlogPostListView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView, download_latest_resume

urlpatterns = [
  path('', home, name='home'),
  # path('home/', views.home, name='home'),

  path('download-latest-resume/', download_latest_resume, name='download_latest_resume'),

  path('posts/', BlogPostListView.as_view(), name='blog-home'),
  path('post/new/', BlogPostCreateView.as_view(), name='blogpost-create'),
  path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blogpost-edit'),
  path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost-delete'),
]