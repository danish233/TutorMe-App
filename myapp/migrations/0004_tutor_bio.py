# Generated by Django 4.1.5 on 2023-04-30 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_tutor_usernm'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='bio',
            field=models.CharField(default='Write a short bio about your skills and experience so students can get to know you better!', max_length=255),
        ),
    ]