# Generated by Django 2.2.4 on 2019-10-27 19:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentview', '0006_registrations_date_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='date_applied',
            field=models.DateField(default=datetime.datetime(2019, 10, 28, 1, 2, 37, 129381)),
        ),
    ]