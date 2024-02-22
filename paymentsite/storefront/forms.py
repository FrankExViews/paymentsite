from django import forms

class BuyCoffeeNowForm(forms.Form):
    CoffeeProdID = forms.CharField()
    CoffeePriceID =forms.CharField()