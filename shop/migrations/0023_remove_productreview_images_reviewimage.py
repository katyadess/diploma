# Generated by Django 5.1 on 2024-08-21 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_rename_image_productreview_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='images',
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='review_images')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_images', to='shop.productreview')),
            ],
        ),
    ]
