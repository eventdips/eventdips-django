# Generated by Django 2.2.4 on 2019-10-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherview', '0017_subevents_confirmation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='subevents',
            name='group_size',
            field=models.IntegerField(default=2),
        ),
    ]
