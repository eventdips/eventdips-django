# Generated by Django 2.2.4 on 2020-01-09 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentview', '0017_auto_20200109_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrations',
            options={'verbose_name_plural': 'Registrations'},
        ),
        migrations.AlterField(
            model_name='registrations',
            name='date_applied',
            field=models.DateField(default=datetime.datetime(2020, 1, 9, 21, 43, 43, 953025)),
        ),
    ]