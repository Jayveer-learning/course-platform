from django.http import Http404
from django.shortcuts import render, HttpResponse

from . import services

# Create your views here.
def course_list_view(request):
    queryset = services.get_publish_course()
    return render(request, "courses/list.html", {})

'''
path("course_detail/<int:id>/", views.course_detail_views, name="Course detail")    
'''
def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404()
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
    return render(request, "courses/lesson.html", {})
