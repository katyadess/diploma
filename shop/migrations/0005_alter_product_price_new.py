# Generated by Django 5.1 on 2024-08-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_price_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_new',
            field=models.DecimalField(blank=True, decimal_places=2, default=10.0, max_digits=10, null=True),
        ),
    ]
