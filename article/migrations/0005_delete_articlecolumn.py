# Generated by Django 2.2 on 2024-01-30 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_articlecolumn'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleColumn',
        ),
    ]