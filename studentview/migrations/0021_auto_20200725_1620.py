# Generated by Django 3.0.8 on 2020-07-25 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentview', '0020_auto_20200111_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='date_applied',
            field=models.DateField(default=datetime.datetime(2020, 7, 25, 16, 20, 21, 479934)),
        ),
    ]
