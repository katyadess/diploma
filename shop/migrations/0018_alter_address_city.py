# Generated by Django 5.1 on 2024-08-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_address_options_remove_address_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=255),
        ),
    ]
