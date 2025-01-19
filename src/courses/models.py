import helpers
from django.db import models
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()

# Create your models here.

'''
    Course:
        title
        description
        thumbnail/image
        Access:
            anyone
            email required
            Purchese required
            User required(n/a)
        status:
            Published
            Coming soon
            Draft
'''

class PublishedStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = 'soon', "Coming soon"
    DRAFT = 'draft', 'Draft'


class AccessRequireme(models.TextChoices):
    ANYONE = 'any', 'Anyone'
    EMAIL_REQUIRED = 'email', 'Email required'

def handle_upload(instance, filename):
    return f'{filename}'

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField("image", null=True)
    access = models.CharField(
        max_length=20, 
        choices=AccessRequireme.choices,
        default=AccessRequireme.EMAIL_REQUIRED
    )
    status = models.CharField(
        max_length=20, 
        choices=PublishedStatus.choices, 
        default=PublishedStatus.DRAFT
    )

    @property
    def is_published(self):
        return self.status == PublishedStatus.PUBLISHED

    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        image_options = {
            "width": 500
        }
        url = self.image.build_url(**image_options) # is same self.image.image(image_options)
        return url

    @property
    def get_image_thumbnail(self, as_html=False, width=650):
        if not self.image:
            return ""
        image_options = {
            "width": width
        }
        if as_html:
            # CloudinaryImage(str(self.image)).image(image_options)
            return self.image.image(**image_options)
        # CloudinaryImage(str(self.image)).build_url(image_options)    
        url = self.image.build_url(**image_options)
        return url

    @property
    def image_tag_admin_url(self):
        if not self.image:
            return ""
        image_options = {
            "width": 100
        }
        url = self.image.build_url(**image_options) # build_url generate url of image
        return url 


    def __str__(self):
        return self.title[:10]



'''
    Lessons
        title
        description
        video
        Status:
            Published
            coming soon
            Draft
'''

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Course')
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, can they see this?")
    status = models.CharField(
        max_length=20, 
        choices=PublishedStatus.choices, 
        default=PublishedStatus.PUBLISHED
    )