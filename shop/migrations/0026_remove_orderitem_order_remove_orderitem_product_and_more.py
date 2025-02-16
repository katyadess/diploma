# Generated by Django 5.1 on 2024-08-25 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_rename_images_reviewimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-created_at'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
