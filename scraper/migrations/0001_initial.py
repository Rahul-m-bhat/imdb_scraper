# Generated by Django 5.2.1 on 2025-05-12 10:42

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MovieDB",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("release_date", models.IntegerField(blank=True, null=True)),
                ("imdb_rating", models.FloatField(blank=True, null=True)),
                ("directors", models.CharField(blank=True, max_length=500, null=True)),
                ("cast", models.TextField(blank=True, null=True)),
                ("plot_summary", models.TextField(blank=True, null=True)),
                ("imdb_url", models.URLField(max_length=500, unique=True)),
            ],
            options={
                "verbose_name_plural": "Movies",
            },
        ),
    ]
