from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

USER_TYPES = [
    ('', 'select'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
]

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student' ,null=True)
    roll_no = models.IntegerField("roll no.",null=True)
    phone_no = PhoneNumberField("Phone No.",null=True)

    def __str__(self):
        return self.username
