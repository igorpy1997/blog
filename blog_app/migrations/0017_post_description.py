# Generated by Django 4.2.4 on 2023-08-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_app", "0016_alter_comment_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="description",
            field=models.CharField(default="", max_length=500),
        ),
    ]
