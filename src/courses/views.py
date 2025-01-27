from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse

from . import services

# Create your views here.
def course_list_view(request):
    queryset = services.get_publish_course()
    return JsonResponse({"data": [x.id for x in queryset]})
    return render(request, "courses/list.html", {})

'''
path("course_detail/<int:id>/", views.course_detail_views, name="Course detail")    
'''
def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404()
    lesson_obj = course_obj.course.all() # using course_obj.lesson_set.all() you can access all related lesson to your course object. instance of lesson_set.all() you can use your related_name that you specified in Foreign_key. lesson_set.all() is defaul and related_name="course" is course.all() same output. so mean this both return related object of specific course obj of Course model.
    return JsonResponse({"data": course_obj.title, "lesson_id": [x.id for x in lesson_obj]})
    return render(request, "courses/detail.html", {})

'''
path("lesson_detail/<int:id>/<int:lesson_id>/", views.course_detail_views, name="Course detail")    
'''
def lesson_list_view(request, id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=id, 
        lesson_id=lesson_id
    )
    if lesson_obj is None:
        raise Http404()
    return JsonResponse({"data": lesson_obj.title})
    return render(request, "courses/lesson.html", {})
