from cloudinary import CloudinaryImage
from django.contrib import admin
from .models import Course
from django.utils.html import format_html

# Register your models here.
@admin.register(Course)
class CourseAdminModel(admin.ModelAdmin):
    list_display = ['image_tag','title', 'status', 'access']
    fields = ['title', 'description', 'image', 'status', 'access', 'display_image']
    list_filter = ['status', 'access']
    readonly_fields = ['display_image']


    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin_url
        return format_html(f"<img src='{url}'/>")

        # another way to do this. 
        '''
        cloudinary_id = str(obj.image) # this return public id of current image. 
        cloudinary_html = CloudinaryImage(cloudinary_id).image(width=500) # CloudinaryImage return html <img src='url of image' />
        return format_html(cloudinary_html)
        '''
    def image_tag(self, obj, *args, **kwargs):
        url = obj.image_tag_admin_url
        return format_html(f"<img src='{url}' width='100px'/>")

    display_image.short_description = 'Current image'