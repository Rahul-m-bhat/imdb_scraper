# Generated by Django 5.2.1 on 2025-05-14 07:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scraper", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="moviedb",
            name="release_date",
        ),
        migrations.AddField(
            model_name="moviedb",
            name="release_year",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
