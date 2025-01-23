import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from .models import Course, Lesson
from django.utils.html import format_html


class LessonInline(admin.StackedInline):
    model = Lesson
    fields = ['public_id', 'title', 'description', 'thumbanil', 'display_thumbnail' , 'video', 'display_video_content', 'order', 'can_preview', 'status', 'updated', 'timestamp']
    readonly_fields = ['public_id', 'updated', 'timestamp', 'display_thumbnail', 'display_video_content']
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

    def display_video_content(self, obj):
        video_embed_html = helpers.get_cloudinary_video_object(
            obj,
            field_name="video",
            as_html=True,
            width=550,
            height=450,
            sign_url=False,
            fetch_format="auto",
            quality="auto"
        )
        return video_embed_html # not need of fotmat_html(video_html) because we using django temlate render that generate html tags so no need for format_html(url). 

    display_video_content.short_description = 'Current Video'

# Register your models here.
@admin.register(Course)
class CourseAdminModel(admin.ModelAdmin):
    inlines = [LessonInline] # inline Lesson class make it oneto many relationship using ForienKey. 
    list_display = ['image_tag','title', 'status', 'access']
    fields = ['public_id','title', 'description', 'image', 'display_image', 'status', 'access', 'timestamp', 'updated']
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