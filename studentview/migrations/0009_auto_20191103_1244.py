# Generated by Django 2.2.4 on 2019-11-03 07:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentview', '0008_auto_20191103_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='date_applied',
            field=models.DateField(default=datetime.datetime(2019, 11, 3, 12, 44, 52, 541330)),
        ),
    ]