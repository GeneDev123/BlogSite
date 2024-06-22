from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import BlogPost, ContactMessage
from .forms import BlogPostForm
from django.conf import settings
from django.utils import timezone
from .models import FileUpload
from django.http import HttpResponse

FB_LINK = settings.FB_LINK
IG_LINK = settings.IG_LINK
GITHUB_LINK = settings.GITHUB_LINK
LINKEDIN_LINK = settings.LINKEDIN_LINK

def home(request):

  social_media_links = {
    'fb_link': FB_LINK,
    'ig_link': IG_LINK,
    'github_link': GITHUB_LINK,
    'linkedin_link': LINKEDIN_LINK,    
  }

  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')

    contact_message = ContactMessage(name=name, email=email, message=message, timestamp=timezone.now())
    contact_message.save()

    return redirect(reverse('home'))

  context = {
    'social_media_links': social_media_links,
  }

  return render(request, 'main/home.html', context)

def download_latest_resume(request):
  latest_resume = FileUpload.objects.filter(category='resume').order_by('-date_modified').first()

  if latest_resume:
    resume_file_path = latest_resume.file.path
    original_filename = latest_resume.file_name

    with open(resume_file_path, 'rb') as resume_file:
      response = HttpResponse(resume_file.read(), content_type='application/octet-stream')
      response['Content-Disposition'] = 'attachment; filename="{}"'.format(original_filename)
      return response

  return HttpResponse('No resume file found.', status=404)

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