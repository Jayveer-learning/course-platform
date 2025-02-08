from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse
import helpers

from . import services

# Create your views here.
'''
path('', views.course_list_view, name='course_list')
'''
# return all course obj that have status in published
def course_list_view(request):
    queryset = services.get_publish_course()
    # return JsonResponse({"data": [x.path for x in queryset]})
    context = {
        "object_list": queryset
    }
    return render(request, "courses/list.html", context)

'''
path("course_detail/<slug:course_public_id>/", views.course_detail_views, name="Course detail")    
'''
# return an specific course obj that match condition value.
def course_detail_view(request, course_public_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_public_id=course_public_id)
    if course_obj is None:
        raise Http404()
    lesson_obj = services.get_course_lessons(course_obj=course_obj) # course object. instance of lesson_set.all() you can use your related_name that you specified in Foreign_key. lesson_set.all() is defaul and related_name="course" is course.all() same output. so mean this both return related object of specific course obj of Course model.
    # return JsonResponse({"data": course_obj.title, "lesson_id": [x.path for x in lesson_obj]})
    context = {
        "object": course_obj,
        "lesson_objects": lesson_obj
    }
    return render(request, "courses/detail.html", context)

'''
path("lesson_detail/<slug:course_public_id>/<slug:lesson_public_id>/", views.course_detail_views, name="Course detail")    
'''
# return an specific lesson obj that match condition value.
def lesson_list_view(request, course_public_id=None, lesson_public_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_public_id=course_public_id, 
        lesson_public_id=lesson_public_id
    )
    if lesson_obj is None:
        raise Http404()
    template_name = "courses/lesson-coming-soon.html"
    context = {
        "lesson": lesson_obj
    }
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        '''
        Execute if lesson is publishe, and video is available.
        '''
        template_name = "courses/lesson.html"
        video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj,
            field_name="video",
            as_html=True,
            width=800,
            sign_url=False,
            fetch_format="auto",
            quality="auto"
        )
        context['video_embed'] = video_embed_html
    # return JsonResponse({"data": lesson_obj.path})
    return render(request, template_name, context)
