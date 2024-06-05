from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm

def home(request):
  return render(request, 'main/home.html', {})

class BlogPostListView(ListView):
  model = BlogPost
  template_name = 'main/blog/posts.html'
  context_object_name = 'posts'
  ordering = ['-created_at']

class BlogPostCreateView(LoginRequiredMixin, CreateView):
  model = BlogPost
  form_class = BlogPostForm
  template_name = 'main/blog/post_form.html'

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse('blog-home')

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = BlogPost
  form_class = BlogPostForm
  template_name = 'main/blog/post_form.html'

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  def test_func(self):
    blogpost = self.get_object()
    return self.request.user == blogpost.author or self.request.user.is_superuser
  
  def get_success_url(self):
    return reverse('blog-home')

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = BlogPost
  success_url = '/'
  template_name = 'main/blog/confirm_delete.html'

  def test_func(self):
    blogpost = self.get_object()
    return self.request.user == blogpost.author or self.request.user.is_superuser
  
  def get_success_url(self):
    return reverse('blog-home')