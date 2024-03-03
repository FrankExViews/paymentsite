from django import forms

class BuyCoffeeNowForm(forms.Form):
    CoffeeProdID = forms.CharField()
    CoffeePriceID =forms.CharField()

class addtocart(forms.Form):
    CartPriceID =forms.CharField()
    CartQuantity = forms.IntegerField()