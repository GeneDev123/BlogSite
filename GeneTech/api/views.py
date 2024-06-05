from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from main.models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
  queryset = BlogPost.objects.all()
  serializer_class = BlogPostSerializer

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

  def get_permissions(self):
    if self.action in ['update', 'partial_update', 'destroy']:
      return [IsAuthenticated()]
    return super().get_permissions()