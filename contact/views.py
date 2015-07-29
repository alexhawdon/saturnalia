from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import SaturnaliaContact
from saturnalia.news.models import NewsItem
from forms import ContactForm
from django.core.mail import send_mail

def contact(request):
    errors = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail('Website Enquiry', 
                      "Message from: " + form.cleaned_data['email']  + "\r\n" + form.cleaned_data['message'], 
                      form.cleaned_data['email'], 
                      [form.cleaned_data['to']])
            return redirect('/contact/thanks/')
        else:
            errors = True
    latest_news = NewsItem.objects.all()[0]
    contacts = SaturnaliaContact.objects.all()
    return render_to_response('contact.html',
                              {'latest_news': latest_news,
                               'contacts': contacts,
                               'errors': errors},
                              context_instance=RequestContext(request))

def thanks(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('contact_thanks.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))
