# Generated by Django 5.1 on 2024-08-21 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_rename_product_wishlist_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productreview',
            old_name='image',
            new_name='images',
        ),
    ]
