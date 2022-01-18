from django.db import models

# Create your models here.
class User(AbstractModel):
    pass

class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    sales_contact = models.ForeignKey('User',
        on_delete=models.CASCADE)


class Contract(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales_contact = models.ForeignKey('User', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()

    
class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    support_contact = models.ForeignKey('User', on_delete=models.CASCADE)
    #event status = models.CharField(choices=) foreign key - int
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
