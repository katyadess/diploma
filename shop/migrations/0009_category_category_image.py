# Generated by Django 5.1 on 2024-08-14 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_product_forth_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.ImageField(blank=True, default=1, null=True, upload_to='categories'),
        ),
    ]
