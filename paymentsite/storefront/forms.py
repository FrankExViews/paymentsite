from django import forms

class BuyCoffeeNowForm(forms.Form):
    CoffeeProdid = forms.HiddenInput