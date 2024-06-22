from django.contrib import admin
from django.utils.html import format_html
from .models import FileUpload, BlogPost, ContactMessage


admin.site.site_header = "GeneTech Admin"

class BlogPostAdmin(admin.ModelAdmin):
  model = BlogPost

  list_display = ('title', 'author', 'created_at', 'updated_at')
  list_filter = ('author', 'created_at', 'updated_at')
  search_fields = ('title', 'content', 'author__username')
  readonly_fields = ('created_at', 'updated_at')

  fieldsets = (
    (None, {
      'fields': ('title', 'content', 'author')
    }),
    ('Timestamps', {
      'fields': ('created_at', 'updated_at'),
      'classes': ('collapse',)
    }),
  )

class FileUploadAdmin(admin.ModelAdmin):
  model = FileUpload

  list_display = ('file_name', 'category', 'date_uploaded', 'date_modified', 'render_media')
  readonly_fields = ('date_uploaded', 'date_modified', 'render_media')
  list_filter = ('category',)

  def render_media(self, obj):
    if obj.category == 'blog_img':
      return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.file.url)
    elif obj.category == 'blog_vid':
      return format_html(
        '<video width="320" height="240" controls>'
        '<source src="{}" type="video/mp4">'
        'Your browser does not support the video tag.'
        '</video>', obj.file.url)
    return ""

  render_media.short_description = 'Media Preview'

# Register the models with their respective admin classes
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(ContactMessage)