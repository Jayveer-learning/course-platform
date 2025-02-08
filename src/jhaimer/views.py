from django.shortcuts import render, redirect
from emails.forms import EmailForm
from django.conf import settings

from emails.models import Email, EmailVerification


def home(request, *args, **kwargs):
    template_name = "web/home.html"
    # forms
    print(request.POST)
    form = EmailForm(request.POST or None)
    context = {
        'email_form': form,
        "message": "Succe"
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email') # cleaned_data.get() Safely retrieves the value, and if the field is missing, it returns None instead of an error. ✅ but if we use only cleaned_data(field_name) give error if form have not user input.  best pratice is use .get()
        # email = form.save()
        email_obj, created = Email.objects.get_or_create(email=email_val) # retirive data from db is email is exits if not this method create an email and return in email_obj that email object created of model Email. 
        obj = EmailVerification.objects.create(
            parent=email_obj,
            email=email_val
        )        
        context['form'] = form
        context['message'] = f"Success! Ckeck yout email for verification from {settings.EMAIL_ADDRESS}"
    else:
        print(form.errors)
    return render(request, template_name, context)