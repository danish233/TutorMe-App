# Generated by Django 4.1.5 on 2023-04-30 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_request',
            name='left_feedback',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutor',
            name='avg_rating',
            field=models.IntegerField(default=11),
        ),
        migrations.AddField(
            model_name='tutor',
            name='number_of_sessions',
            field=models.IntegerField(default=0),
        ),
    ]