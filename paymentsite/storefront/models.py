from django.db import models

# Create your models here.

class stripeorders(models.Model):
    stripe_order_num = models.CharField(max_length=50,primary_key=True)
    stripe_order_username = models.CharField(max_length=50)
    stripe_ship_status = models.CharField(max_length=10)

    def __str__(self):
        return self.stripe_order_num,self.stripe_order_username,self.stripe_ship_status,

#class stripshoppingcart(models.Model):
 #   cart_item_username = models.CharField(max_length=50)
# cart_item_qty=models.CharField(max_length=4)
  #  cart_item_priceid=models.CharField(max_length=50)



class stripeshoppingcart(models.Model):
    cart_item_username = models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    quantity=models.IntegerField()
    adjustable_quantity=models.CharField(max_length=50)