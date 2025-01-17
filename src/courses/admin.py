from django.contrib import admin
from .models import Course

# Register your models here.
@admin.register(Course)
class CourseAdminModel(admin.ModelAdmin):
    list_display =['title', 'status', 'access']
    fields = ['title', 'description', 'image', 'status', 'access']
    list_filter = ['status', 'access']