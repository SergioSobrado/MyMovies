# Generated by Django 4.2.6 on 2023-10-23 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_person_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='biography',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
