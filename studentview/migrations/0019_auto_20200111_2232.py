# Generated by Django 2.2.4 on 2020-01-11 17:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentview', '0018_auto_20200109_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='date_applied',
            field=models.DateField(default=datetime.datetime(2020, 1, 11, 22, 32, 10, 944859)),
        ),
    ]
