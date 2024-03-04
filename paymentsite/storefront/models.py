from django.db import models

# Create your models here.

class stripeorders(models.Model):
    stripe_order_num = models.CharField(max_length=50,primary_key=True)
    stripe_order_email = models.CharField(max_length=50)
    stripe_ship_status = models.CharField(max_length=10)
    stripe_shipping_address=models.CharField(max_length=255,default='DEFAULT')
    stripe_receipt_url=models.CharField(max_length=255,default='DEFAULT')


class stripeshoppingcart(models.Model):
    cart_item_username = models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    quantity=models.IntegerField()
    adjustable_quantity=models.CharField(max_length=50)
