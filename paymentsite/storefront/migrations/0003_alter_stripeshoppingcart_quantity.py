# Generated by Django 4.2.9 on 2024-03-03 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0002_alter_stripeshoppingcart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripeshoppingcart',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
