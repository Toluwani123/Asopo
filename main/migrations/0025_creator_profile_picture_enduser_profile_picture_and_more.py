# Generated by Django 4.1.6 on 2023-07-17 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0024_remove_creator_profession_remove_enduser_required_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="creator",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="creator-pictures/"
            ),
        ),
        migrations.AddField(
            model_name="enduser",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="enduserpictures/"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="demo_picture_1",
            field=models.ImageField(
                blank=True, null=True, upload_to="projectpictures/"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="demo_picture_2",
            field=models.ImageField(
                blank=True, null=True, upload_to="projectpictures/"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="demo_picture_3",
            field=models.ImageField(
                blank=True, null=True, upload_to="projectpictures/"
            ),
        ),
    ]
