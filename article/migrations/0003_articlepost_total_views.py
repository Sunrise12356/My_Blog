# Generated by Django 2.2 on 2024-01-30 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20240129_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='total_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]