# Generated by Django 2.2.4 on 2020-01-09 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherview', '0021_auto_20200108_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='security_answers',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='security_questions',
            field=models.TextField(default='temp'),
            preserve_default=False,
        ),
    ]
