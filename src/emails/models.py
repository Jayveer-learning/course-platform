from django.db import models

# Create your models here.
'''
Email verification for short-lived access
    -Views:
        - Collect user email
        - Vevify user email
            - Activate session
    
    -Models:
        - Email
        - EmailVerificationToken
'''

class Email(models.Model):
    email = models.EmailField(unique=True)
    activate = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class EmailVerification(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True, related_name="user_email")
    email = models.EmailField()
    # token
    attempts = models.IntegerField(null=True)
    last_attempt_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        blank=True,
        null=True
    )
    expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)