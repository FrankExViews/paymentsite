from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stripe import stripe
import re
import json
from .forms import BuyCoffeeNowForm,addtocart
from storefront.models import stripeorders,stripeshoppingcart

# Create your views here.

stripe.api_key=settings.STRIPE_PRIVATE_KEY
mailchimpkey=settings.MAILCHIMP_API_KEY
mailchimptransactionkey=settings.MAILCHIMP_API_TRANSACTION_KEY
webhook=settings.WEBHOOK


#create a webhook from Stripe API to Render webhook. 
#endpoint = stripe.WebhookEndpoint.create(
 # url='https://api.render.com/deploy/srv-cn51vsmn7f5s7394baig?key=8kOv_I__8sU',
  #enabled_events=[
   # 'payment_intent.payment_failed',
    #'payment_intent.succeeded',
  #],
#)

#sample STRIPE WEBHOOK code to capture events
@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  event = None

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    # Then define and call a method to handle the successful payment intent.
    # handle_payment_intent_succeeded(payment_intent)
  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    # Then define and call a method to handle the successful attachment of a PaymentMethod.
    # handle_payment_method_attached(payment_method)
  # ... handle other event types
  else:
    print('Unhandled event type {}'.format(event.type))

  return HttpResponse(status=200)

# this function is run anytime you visit/refresh a 'buy coffee' or 'buy equipment' page
# this is run each time to make sure the latest values,images etc.. for the products listed in Stripe, are returned by Stripe
# note: a key:value pair needs to be added to each product in Stripe, coffe:coffee for any coffee products
# and equipment:typeofequipment for equipment. Python templates used on htmal pages filter based off these key/value pairs.
# make sure to add the metadata to a new product after adding a new product to stripe.
def getfreshupdates():

    allproducts=stripe.Product.list()
    allprices=stripe.Price.list()
    producturls={}

    products = stripe.Product.list()
    # Iterate through the products and get a url for the product picture
    for i in products.auto_paging_iter():
        if i.active==True:
            string=str(i.images)
            #regex to remove characters to a get a 'correct' url to use as an image source.
            newstring=re.sub(r'[\[\]\']','',string)
            newid=i.id
            producturls.update({newid:newstring})

    #use Stripe API auto_paging_iter to get a list of products, that Python can iterate through.
    for i in products.auto_paging_iter():
        allproductsupdated=allproducts
    return(allproductsupdated,allprices,producturls)

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

#test mail to notify me of a server reboot and prove mail functionality works upon server reboot.
mailchimp = MailchimpTransactional.Client(mailchimptransactionkey)
message = {
    "from_email": "coffee@bigbootcoffee.com",
    "subject": "Server Started",
    "text": "Server Started",
    "to": [
      {
        "email": "keithanolan@gmail.com",
        "type": "to"
      }
    ]
}


def run():
 try:
    response = mailchimp.messages.send({"message":message})
    print('API called successfully: {}'.format(response))

 except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))
 

run()



def home(request):
    return render(request,'storefront/home.html',)

def buyequipment(request):
    allproductsupdated,allprices,producturls=getfreshupdates()

    if request.method == 'POST':
        #below is the "buy now" post to trigger a unlogged in users buy now purchase
        if 'CoffeeProdID' in request.POST:
          form = BuyCoffeeNowForm(request.POST)
          if form.is_valid():
            Product_ID=form.cleaned_data.get('CoffeeProdID')
            PRICE_ID=form.cleaned_data.get('CoffeePriceID')
           #below Im testing if the cart can be specified as a variable, which it can.
            cart=[{
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': PRICE_ID,
                    'quantity': 1,
                    'adjustable_quantity':{'enabled':True,"minimum": 1,},
                }]
            print(cart)
            checkout_session = stripe.checkout.Session.create(
            line_items=cart,
            mode='payment',
            billing_address_collection='required',
            shipping_address_collection={"allowed_countries":['IE']},
            success_url='https://retailsiteweb.onrender.com/',
            cancel_url='https://retailsiteweb.onrender.com/',
        )
            return redirect(checkout_session.url, code=303)
   #bewlow is the add product to cart option for a user that is logged in.
    if 'CartPriceID' in request.POST:
           form = addtocart(request.POST)
           if form.is_valid():
            PRICE_ID=form.cleaned_data.get('CartPriceID')
            user=request.user.username
            newcartitem=stripeshoppingcart(cart_item_username=user,price=PRICE_ID, quantity=1,)
            newcartitem.save()
            allcartitems=stripeshoppingcart.objects.filter(cart_item_username=user).values()
            print(allcartitems)
            allproductsupdated,allprices,producturls=getfreshupdates()
            return redirect('/cart/',{'allcartitems':allcartitems,'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

    return render(request,'storefront/buyequipment.html',{'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

def buycoffee(request):
    allproductsupdated,allprices,producturls=getfreshupdates()

    if request.method == 'POST':
        #below is the "buy now" post to trigger a unlogged in users buy now purchase
        if 'CoffeeProdID' in request.POST:
          form = BuyCoffeeNowForm(request.POST)
          if form.is_valid():
            Product_ID=form.cleaned_data.get('CoffeeProdID')
            PRICE_ID=form.cleaned_data.get('CoffeePriceID')
            print(Product_ID)
            print(PRICE_ID)
            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': PRICE_ID,
                    'quantity': 1,
                    'adjustable_quantity':{'enabled':True,"minimum": 1,},
                },
            ],
            mode='payment',
            billing_address_collection='required',
            shipping_address_collection={"allowed_countries":['IE']},
            success_url='https://retailsiteweb.onrender.com/',
            cancel_url='https://retailsiteweb.onrender.com/',
            )
            return redirect(checkout_session.url, code=303)
          #bewlow is the add product to cart option for a user that is logged in.
        if 'CartPriceID' in request.POST:
           form = addtocart(request.POST)
           if form.is_valid():
            PRICE_ID=form.cleaned_data.get('CartPriceID')
            user=request.user.username
            newcartitem=stripeshoppingcart(cart_item_username=user,price=PRICE_ID, quantity=1)
            newcartitem.save()
            allcartitems=stripeshoppingcart.objects.filter(cart_item_username=user).values()
            print(allcartitems)
            allproductsupdated,allprices,producturls=getfreshupdates()
            return redirect('/cart/',{'allcartitems':allcartitems,'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})  
    return render(request,'storefront/buycoffee.html',{'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

def faq(request):
    return render(request,'storefront/faq.html',)

def about(request):
    return render(request,'storefront/about.html',)

#below is the view cart request, it will do a DB check to see if there are any items for the logged in user in the cart already.
def cart(request):
   user=request.user.username
   allcartitems=stripeshoppingcart.objects.filter(cart_item_username=user).values()
   print(allcartitems)
   allproductsupdated,allprices,producturls=getfreshupdates()

   if request.method == 'POST':
    if 'Delete Cart' in request.POST:
       user=request.user.username
       stripeshoppingcart.objects.filter(cart_item_username=user).delete()
       return render(request,'storefront/cart.html')
  
   if 'Checkout' in request.POST:
       #collect all cart items in database and write them in JSON format to a variable json_data
       allcartitems=stripeshoppingcart.objects.filter(cart_item_username=user).values('price','quantity')
       json_data = json.dumps(list(allcartitems))
       #in order to be able to correctly submit the json data stored in json_data, I use json.loads to create a new variable
       #if this step is not performed, Stripe will give an "invalid array" error when attmepting to create a checkout session.
       #while the content of json_data is correct and if you print out and use the contents in code, it will work.
       #Stripe does not seem to pick up the contents of the json_data variable correctly.
       #json.loads () to a new varialbe resovles the issue as the json data is storaed as a variable that Python handles correctly....   
       test=json.loads(json_data)

       checkout_session = stripe.checkout.Session.create(
            line_items=test,
            mode='payment',
            billing_address_collection='required',
            shipping_address_collection={"allowed_countries":['IE']},
            success_url='https://retailsiteweb.onrender.com/',
            cancel_url='https://retailsiteweb.onrender.com/',
      )
       return redirect(checkout_session.url, code=303)
       

   return render(request,'storefront/cart.html',{'allcartitems':allcartitems,'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})  