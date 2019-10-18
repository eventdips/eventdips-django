# Generated by Django 2.2.4 on 2019-10-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('registration_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=64)),
                ('student_class', models.IntegerField()),
                ('student_section', models.CharField(max_length=1)),
                ('event_id', models.IntegerField()),
                ('subevent_id', models.IntegerField()),
                ('reg_info', models.TextField()),
                ('acheivements', models.TextField()),
                ('reg_status', models.CharField(max_length=1)),
            ],
        ),
    ]
