from django.urls import path
from .views import home, BlogPostListView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

urlpatterns = [
  path('', home, name='home'),
  # path('home/', views.home, name='home'),

  path('posts/', BlogPostListView.as_view(), name='blog-home'),
  path('post/new/', BlogPostCreateView.as_view(), name='blogpost-create'),
  path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blogpost-edit'),
  path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost-delete'),
]