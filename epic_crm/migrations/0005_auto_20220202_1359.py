# Generated by Django 3.2.11 on 2022-02-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic_crm', '0004_auto_20220127_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(),
        ),
        
    ]
