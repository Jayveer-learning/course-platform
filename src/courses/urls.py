from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail_view, name='Course_detail'), 
    path('courses/<int:id>/lessons/<int:lesson_id>/', views.lesson_list_view, name='Course_detail'), 
]
