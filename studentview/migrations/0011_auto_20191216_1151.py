# Generated by Django 2.2.4 on 2019-12-16 06:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentview', '0010_auto_20191212_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrations',
            name='group_ids',
        ),
        migrations.AddField(
            model_name='registrations',
            name='event_type',
            field=models.CharField(default='I', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registrations',
            name='date_applied',
            field=models.DateField(default=datetime.datetime(2019, 12, 16, 11, 51, 14, 888740)),
        ),
    ]