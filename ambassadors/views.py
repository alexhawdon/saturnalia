from django.shortcuts import render_to_response, redirect
from saturnalia.shop.models import Balance, Ticket, Deposit, Order, OrderState
from forms import RegistrationForm, ChangePasswordForm, ClaimSaleForm
from models import Ambassador, SaleClaim
from django.core.mail import send_mail
from django.template import RequestContext
import datetime
from saturnalia.news.models import NewsItem
from django.contrib.auth.models import User

AMBASSADOR_SCHEME_FINISH = datetime.date(year=2011, month=7, day=8) #Friday 8th July, two weeks before festival

def about(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('ambassador_about.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/login-required')
    else:
        return render_to_response('dashboard.html',
            {'scheme_finish': AMBASSADOR_SCHEME_FINISH,
             'top10': Ambassador.objects.top10()},
             context_instance=RequestContext(request)
            )
    
def register(request):
    latest_news = NewsItem.objects.all()[0]
    if request.method == 'POST': #User is attempting submit registration form
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #Create the user objects, w fake username hashed from email address
            user = User(username=str(hash(form.cleaned_data['email'])),
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            #Now create associated ambassador instance
            ambassador = Ambassador(user = user,
                                    code=form.cleaned_data['code'],
                                    target=form.cleaned_data['target'],
                                    phone=form.cleaned_data['phone'],
                                    nickname=form.cleaned_data['ambassador_nickname'])
            ambassador.save()
            
            send_mail('Summer Saturnalia | Ambassador registration confirmation',
                      '''Congratulations!  You are now registered as a Summer Saturnalia ambassador.
Log in using your email address and password at the 'login' link at the top of www.summersaturnalia.com.
If you have any questions that the FAQ doesn't answer then don't hesitate to get in touch.

Love from Team Summer Saturnalia :)''',
                      'enquiries@summersaturnalia.com',
                      [form.cleaned_data['email']],
                      fail_silently=False)
            return redirect('/ambassador/registration_successful')
    else: #User would like to see registration form
        form = RegistrationForm()
    
    return render_to_response('register.html', 
                              {'registration_form': form,
                               'latest_news': latest_news},
                              context_instance=RequestContext(request))

def registration_successful(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('registration_successful.html', {'latest_news': latest_news})

def change_password(request):
    latest_news = NewsItem.objects.all()[0]
    if not request.user.is_authenticated():
        return redirect('/login-required')
    else:
        if request.method == 'POST':
            form = ChangePasswordForm(data=request.POST, user=request.user)
            if form.is_valid():
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                return redirect('/ambassador/password-change-successful')
        else:
            form = ChangePasswordForm(request.user)
        return render_to_response("change_password.html",
                                  {'change_password_form': form,
                                   'latest_news': latest_news},
                                  context_instance=RequestContext(request))

def password_change_successful(request):
    latest_news = NewsItem.objects.all()[0]
    if not request.user.is_authenticated():
        return redirect('/login-required')
    else:
        return render_to_response("password_change_successful.html",
                                  {'latest_news': latest_news},
                                  context_instance=RequestContext(request))
                                  
def claim_sale(request):
    latest_news = NewsItem.objects.all()[0]
    if not request.user.is_authenticated():
        return redirect('/login-required')
    else:
        current_claims = SaleClaim.objects.filter(ambassador=request.user.get_profile())
        if request.method == 'POST':
            form = ClaimSaleForm(request.POST)
            if form.is_valid():
                claim = SaleClaim(ambassador = request.user.get_profile(),
                                  fname = form.cleaned_data['fname'],
                                  lname = form.cleaned_data['lname'],
                                  email = form.cleaned_data['email'],
                                  phone = form.cleaned_data['phone'],
                                  other_details = form.cleaned_data['other_details'])
                claim.save()
                return redirect('/ambassador/claim-registered')
        else:
            form = ClaimSaleForm()
        return render_to_response('claim_sale.html',
                                 {'saleClaimForm': form,
                                  'outstandingClaims': current_claims,
                                  'latest_news': latest_news},
                                  context_instance=RequestContext(request))
def claim_registered(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('claim_registered.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))
