# Generated by Django 2.2.11 on 2022-01-24 05:50

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20220124_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='input_image',
            field=models.ImageField(blank=True, upload_to=home.models.image_name),
        ),
    ]
