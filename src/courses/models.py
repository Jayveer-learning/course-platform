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


    def __str__(self):
        return self.title[:10]
    