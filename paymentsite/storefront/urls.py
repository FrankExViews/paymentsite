from django.urls import path
from .import views

urlpatterns= [

path('',views.home, name='home'),
path('buyequipment/',views.buyequipment, name='buyequipment'),
path('buycoffee/',views.buycoffee, name='buycoffee'),
path('faq/',views.faq, name='faq'),
path('about/',views.about, name='about'),
path('cart/',views.cart, name='cart'),
]