import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from .models import Course, Lesson
from django.utils.html import format_html


class LessonInline(admin.StackedInline):
    model = Lesson
    fields = ['public_id', 'title', 'description', 'thumbanil', 'display_thumbnail' , 'video', 'order', 'can_preview', 'status', 'updated', 'timestamp']
    readonly_fields = ['public_id', 'updated', 'timestamp', 'display_thumbnail']
    extra = 0 # means number of empty forms display in admin panel for adding lessons ok. 

    def display_thumbnail(self, obj):
        url = helpers.get_cloudinary_image_object(
            obj,
            field_name="thumbanil",
            as_html=False,
            width=300
        )
        return format_html(f"<img src='{url}' />")

    display_thumbnail.short_description = 'Current Thumbail'

# Register your models here.
@admin.register(Course)
class CourseAdminModel(admin.ModelAdmin):
    inlines = [LessonInline] # inline Lesson class make it oneto many relationship using ForienKey. 
    list_display = ['image_tag','title', 'status', 'access']
    fields = ['public_id','title', 'description', 'image', 'status', 'access', 'display_image', 'timestamp', 'updated']
    list_filter = ['status', 'access']
    readonly_fields = ['public_id', 'display_image', 'timestamp', 'updated']


    def display_image(self, obj, *args, **kwargs):
        # url = obj.image_admin_url
        url = helpers.get_cloudinary_image_object(
            obj,
            field_name="image",
            as_html=False,
            width=400
        )
        return format_html(f"<img src='{url}'/>")

        # another way to do this. 
        '''
        cloudinary_id = str(obj.image) # this return public id of current image. 
        cloudinary_html = CloudinaryImage(cloudinary_id).image(width=500) # CloudinaryImage return html <img src='url of image' />
        return format_html(cloudinary_html)
        '''
    def image_tag(self, obj, *args, **kwargs):
        # url = obj.image_tag_admin_url # old approach
        url = helpers.get_cloudinary_image_object(            
            obj,
            field_name="image",
            as_html=False,
            width=100)
        return format_html(f"<img src='{url}' />")

    display_image.short_description = 'Current image' # add sort name of any field and make more user friendly admin page. 