# Generated by Django 2.2.4 on 2020-01-29 14:02

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
            field=models.DateField(default=datetime.datetime(2020, 1, 29, 19, 32, 8, 53703)),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='rej_reason',
            field=models.TextField(null=True),
        ),
    ]
