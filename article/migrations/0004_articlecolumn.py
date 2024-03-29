# Generated by Django 2.2 on 2024-01-30 08:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_articlepost_total_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
