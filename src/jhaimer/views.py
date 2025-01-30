from django.shortcuts import render


def home(request, *args, **kwargs):
    template_name = "web/home.html"
    return render(request, template_name)