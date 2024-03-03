# Generated by Django 4.2.9 on 2024-03-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stripeorders',
            fields=[
                ('stripe_order_num', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('stripe_order_username', models.CharField(max_length=50)),
                ('stripe_ship_status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='stripeshoppingcart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_item_username', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=50)),
                ('quantity', models.CharField(max_length=4)),
                ('adjustable_quantity', models.CharField(max_length=50)),
            ],
        ),
    ]
