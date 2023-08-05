# Generated by Django 4.2.4 on 2023-08-01 19:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_app", "0002_rename_image_siteimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("title", models.CharField(max_length=100)),
                ("photo", models.ImageField(upload_to="images/")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("header", "Header Image"),
                            ("profile", "Profile Image"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="SiteImage",
        ),
    ]