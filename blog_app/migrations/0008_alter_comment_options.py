# Generated by Django 4.2.4 on 2023-08-08 16:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog_app", "0007_comment_created_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["created_at"]},
        ),
    ]
