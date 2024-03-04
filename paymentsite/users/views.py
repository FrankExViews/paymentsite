from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #import for messages
from .forms import UserRegisterForm  #Import added
from django.shortcuts import redirect
from django.conf import settings
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

mailchimpkey=settings.MAILCHIMP_API_KEY
mailchimptransactionkey=settings.MAILCHIMP_API_TRANSACTION_KEY

# Create your views here.

def SendRegMsg(emailsend):
    print('execute')
    print('emailsend::'+emailsend)
    mailchimp = MailchimpTransactional.Client(mailchimptransactionkey)
    message = {
    "from_email": "register@bigbootcoffee.com",
    "subject": "Welcome to Bigboot Coffee",
    "text": "Welcome to Bigboot Coffee! Your Account has been registered.",
    "to": [
    {
    "email": emailsend,
    "type": "to"
    }
    ]
    }
    response = mailchimp.messages.send({"message":message})
    print('API called successfully: {}'.format(response))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            emailsend = form.cleaned_data.get('email')
            SendRegMsg(emailsend)
            
        return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})




