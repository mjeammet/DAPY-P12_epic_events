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

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Contract(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    client = models.ForeignKey(to='Client', on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()

    
class Event(models.Model):
    EVENT_STATUS = (
        ('FUTURE', 'Future event'),
        ('PAST', 'Past event'),
    )

    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(to='Client', on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    #event_status = models.CharField(choices=) foreign key - int
    # event_status = models.CharField(choices=EVENT_STATUS, max_length=6, default=EVENT_STATUS.FUTURE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=2048, blank=True)
