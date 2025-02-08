from . import css
from django import forms
from .models import (
    Email
)

# now we are going to using form just for validation. means user put all information correct, clean, securely before saving data into database. 

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs = {
                'id': "email-login-input",
                "class": css.EMAIL_FIELD_CSS,
                "placeholder": "Your Email"
            }
        )
    )
    # class Meta:
    #     model = Email
    #     fields = ["email"]

    # validation methods 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Email.objects.filter(email=email, activate=False)
        if qs.exists():
            raise forms.ValidationError("Invalid email type")
        return email