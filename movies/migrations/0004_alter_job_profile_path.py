# Generated by Django 4.2.6 on 2023-10-22 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_job_profile_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='profile_path',
            field=models.URLField(blank=True, null=True),
        ),
    ]
