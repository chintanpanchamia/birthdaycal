from __future__ import unicode_literals

import string
import random

from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    email_subject = models.CharField(max_length=512, default="Many happy returns!")
    email_body = models.TextField(default=("Dear [fn] [ln], \n\nMany happy returns!\n\nWarm regards,\nDr. {0}"))

    def set_random_password(self):
        user = self.user
        chars = string.letters + string.digits + string.punctuation
        pswd = ''.join((random.choice(chars) for x in range(20)))
        user.set_password(pswd)
        user.save()
        return pswd

    def __str__(self):
        return self.last_name


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    dob = models.DateTimeField()
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return self.email