from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stripe import stripe
import re
import json
from .forms import BuyCoffeeNowForm,addtocart
from storefront.models import stripeorders,stripshoppingcart

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

mailchimp = MailchimpTransactional.Client(mailchimptransactionkey)
message = {
    "from_email": "coffee@bigbootcoffee.com",
    "subject": "Hello world",
    "text": "Welcome to Mailchimp Transactional!",
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
        form = BuyCoffeeNowForm(request.POST)
        if form.is_valid():
            Product_ID=form.cleaned_data.get('CoffeeProdID')
            PRICE_ID=form.cleaned_data.get('CoffeePriceID')
            print(Product_ID)
            print(PRICE_ID)
            print(webhook)
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

    return render(request,'storefront/buyequipment.html',{'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

def buycoffee(request):
    allproductsupdated,allprices,producturls=getfreshupdates()

    if request.method == 'POST':
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
        if 'CartPriceID' in request.POST:
           form = addtocart(request.POST)
           if form.is_valid():
            PRICE_ID=form.cleaned_data.get('CartPriceID')
            user=request.user.username
            newcartitem=stripshoppingcart(cart_item_username=user,cart_item_priceid=PRICE_ID, cart_item_qty=1)
            newcartitem.save()


           return render(request,'storefront/cart.html')  
    return render(request,'storefront/buycoffee.html',{'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

def faq(request):
    return render(request,'storefront/faq.html',)

def about(request):
    return render(request,'storefront/about.html',)

{
            
        }