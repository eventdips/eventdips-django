# Generated by Django 2.2.4 on 2019-10-19 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studentview', '0002_delete_registrations'),
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
                ('group_ids', models.CharField(max_length=256)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]