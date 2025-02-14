from .models import (
    Course,
    PublishedStatus,
    Lesson
)
from django.db.models import Q

# return all course obj that have status in published
def get_publish_course():
    return Course.objects.filter(status=PublishedStatus.PUBLISHED) # return objects if status field of course is Published so we use PublishedStatus,PUBLISHED class for filtering the Course objects. 


# return an specific course obj that match condition value.
def get_course_detail(course_public_id=None):
    if course_public_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(
            status=PublishedStatus.PUBLISHED,
            public_id=course_public_id
        ) # so get data from Course objects that have status is published and id is equal to course_id is both value match then get method get the object from Course models database. and then return obj.  
    except Exception as err:
        print(f"Course Data Query Error: {err}")
    return obj

def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none() # instance of lessons = [] you can also write this Lesson.objects.none() return None with same datatype is queryset. it does not effect code but it's good to return same datatype what we expect. 
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.course.filter(  # reverse relationship to all related object/models. 
        course__status=PublishedStatus.PUBLISHED
    ).filter(
        Q(status=PublishedStatus.PUBLISHED) | 
        Q(status=PublishedStatus.COMING_SOON)
    )
    return lessons

# return an specific lesson obj that match condition value.
def get_lesson_detail(course_public_id=None, lesson_public_id=None):
    if course_public_id is None or lesson_public_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_public_id, # double underscore is use to travel foreign key relationship in django orm. means you can access from lesson course field. 
            course__status=PublishedStatus.PUBLISHED, # double underscore use to travel model relationship and access. 
            status__in=[PublishedStatus.PUBLISHED, PublishedStatus.COMING_SOON], # lesson status
            public_id=lesson_public_id
        )# in this if course__id=course_id. status of lesson course if is public course__status=PublishedStatus.PUBLISHED and id of lesson model if equal to that we provide id=lesson_id if all of this data match then get method get then data of lesson object return. 
    except Exception as err:
        print(f"Lesson Data Query Error: {err}")
    return obj

