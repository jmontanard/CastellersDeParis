from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from location_field.models.plain import PlainLocationField


# Create your models here.

class Casteller(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    user = models.ForeignKey(User, blank=True)
    mail = models.EmailField(blank=True)
    birthday = models.DateField()
    phone = PhoneNumberField(blank=True)


class EventType(models.Model):
    name = models.CharField(max_length=20)


class Event(models.Model):
    type = models.ForeignKey(EventType)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=False)
    date = models.DateField()
    time = models.TimeField()
    location_name = models.CharField(max_length=50)
    location = PlainLocationField(based_fields=['location_name'],
                                  blank=True)
