# Generated by Django 4.2.5 on 2023-10-04 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoupload', '0011_video_share_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_blob_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
