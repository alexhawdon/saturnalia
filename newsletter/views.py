from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import NewsletterForm
from models import Newsletter
from saturnalia.news.models import NewsItem

def newsletter(request):
    latest_news = NewsItem.objects.all()[0]
    if request.method == 'POST':
        #Attempting to register
        form = NewsletterForm(request.POST)
        if form.is_valid():
            signup = Newsletter(name = form.cleaned_data['name'],
                                email = form.cleaned_data['email'])
            signup.save()
            return redirect('/newsletter/signup-successful/')
    else:
        form = NewsletterForm()
    
    return render_to_response('newsletter.html',
                              {'form': form,
                               'latest_news': latest_news},
                              context_instance=RequestContext(request))

def signup_successful(request):
    latest_news = NewsItem.objects.all()[0]
    
    return render_to_response('signup_successful.html',
                              {'latest_news': latest_news},
                               context_instance=RequestContext(request))
