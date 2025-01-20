import helpers
import uuid
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


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

def handle_upload(instance, filename): # instance is name of model where this fn set. 
    return f'{filename}'

def get_public_id_prefix(instance, *args, **kwargs): # instance mean current working model 
    title = instance.title 
    if title:
        slug = slugify(title)
        unique_id= str(uuid.uuid4()).replace("-", "")[:5]
        return f"courses/{instance.id}/{slug}-{unique_id}"
    if instance.id:
        return f"courses/{instance.id}"
    return "courses"

def get_display_name(instance, *args, **kwargs): # display_name refers to a human-readable name for a media asset. It is used for display purposes in the Cloudinary Media Library, making it easier to identify and manage files donn't effect accessed, delivered of media assets. Just for human readability in the Cloudinary UI. it doesn't effect url only display in cloudinary dashboard. 
    title = instance.title 
    if instance.title:
        return title
    return "Course Upload"

def get_tags(instance, *args, **kwargs):
    return ["course", "Thumbnail"]


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField(
        "image", 
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=get_tags
    )
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
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    @property
    def is_published(self):
        return self.status == PublishedStatus.PUBLISHED # return trun if self.status == to PublishedStatus.PUBLISHED if not return false. 

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
        return self.title



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
'''
to  accessing lesson we can access using 

lesson_obj = course_lesson.all()
''' 

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Course')
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    thumbanil = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField(
        "video", 
        blank=True, 
        null=True,
        resource_type="video"
    )
    order = models.IntegerField(default=0) # defining the order of lesson model updating and creation display first lesson that created resently. 
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, can they see this?")
    status = models.CharField(
        max_length=20, 
        choices=PublishedStatus.choices, 
        default=PublishedStatus.PUBLISHED
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated'] # 
        """
        Meta options for the model.
        Attributes:
            ordering (list): Specifies the default ordering for the model's objects.
                The ordering is based on the 'order' field in ascending order by default.
                This means that when querying the model using `course__lesson.objects.all()`,
                the results will be fetched from the database in ascending order of the lessons.
        Notes:
            - The default ordering is ascending (smaller to higher).
            - You can change the ordering when fetching data by using `course__lesson.objects.filter().order_by("-order")`
              to get the data in descending order lessons.
        """