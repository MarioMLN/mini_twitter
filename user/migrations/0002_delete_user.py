# Generated by Django 3.2.25 on 2024-10-28 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20241028_0054'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
