# Generated by Django 5.1 on 2024-08-21 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_remove_productreview_images_reviewimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewimage',
            old_name='image',
            new_name='images',
        ),
    ]
