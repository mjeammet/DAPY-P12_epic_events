from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    TEAMS = (
        ('ADMIN', 'Admin team, managing users and accessing all data'),
        ('SALES', 'Sales team, managing clients and contracts'),
        ('SUPPORT', 'Suppport team, managing events'),
    )
    
    team = models.CharField(choices=TEAMS, max_length=7)

    # @property
    # def username(self):
    #     return f'{self.first_name[0].lower()}{self.last_name.lower()}'



class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)


    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.email}'


class Contract(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    client = models.ForeignKey(to='Client', on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_signed = models.BooleanField() # Previously "status"
    amount = models.FloatField()
    payment_due = models.DateTimeField()

    
class Event(models.Model):
    INCOMING_EVENT = "incoming"
    COMPLETED_EVENT = "over"
    EVENT_STATUS = [
        (INCOMING_EVENT, 'Future event'),
        (COMPLETED_EVENT, 'Past event'),
    ]

    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(to='Client', on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    event_status = models.CharField(choices=EVENT_STATUS, max_length=20, default=INCOMING_EVENT) # Not Foreign Key but tuple
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=2048, blank=True)
