from django.shortcuts import render
from django.conf import settings
from stripe import stripe
import re

# Create your views here.

stripe.api_key=settings.STRIPE_PRIVATE_KEY
mailchimpkey=settings.MAILCHIMP_API_KEY
mailchimptransactionkey=settings.MAILCHIMP_API_TRANSACTION_KEY


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
    return render(request,'storefront/buyequipment.html',{'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

def buycoffee(request):
    allproductsupdated,allprices,producturls=getfreshupdates()
    return render(request,'storefront/buycoffee.html',{'allproductsupdated':allproductsupdated,'allprices':allprices,'producturls':producturls})

def faq(request):
    return render(request,'storefront/faq.html',)

def about(request):
    return render(request,'storefront/about.html',)

{
            
        }