from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template import RequestContext
from saturnalia.news.models import NewsItem

##Static pages

def about(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('about.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def terms_and_conditions(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('terms_and_conditions.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def home(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('home.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))
def whats_on(request):
    return render_to_response('whats_on.html', context_instance=RequestContext(request))

def arenas(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('arenas.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def art(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('art.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def activities(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('activities.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def ameneties(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('ameneties.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def film(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('film.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def social_media(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('social_media.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

##Auth handling

def login(request):
    auth.logout(request)
    latest_news = NewsItem.objects.all()[0]
    username = str(hash(request.POST.get('username', '')))
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to dashboard
        return redirect("/ambassador/dashboard/")
    else:
        # Problem with username or password
        return render_to_response('login.html',
                                  {'latest_news': latest_news},
                                  context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect('/')

def login_required(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('login_required.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))

def forgotten_password(request):
    latest_news = NewsItem.objects.all()[0]
    if request.method == 'POST': #User is trying to reset their password
        email = request.POST.get('email', '')
        try:
            user = auth.models.User.objects.get(username=int(hash(email)))
            new_password = auth.models.User.objects.make_random_password(length=6)
            user.set_password(new_password)
            user.save()
            message='''You have recieved this message because you have forgotten your password and requested for it to be reset.
Your new password is %s
After logging in you can change your password to one of your choosing via the Ambassador Dashboard.''' %new_password
            
            user.email_user(subject='Summer Saturnalia | Forgotten Password', message=message)
            return redirect('/reset-sent/')
        except auth.models.User.DoesNotExist:
            #No user with that email
            return render_to_response('forgotten_password.html', {'status': 'no_such_user', 'latest_news': latest_news}, context_instance=RequestContext(request))
    else:
        return render_to_response('forgotten_password.html',{'latest_news': latest_news}, context_instance=RequestContext(request))

def reset_sent(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('reset_sent.html',{'latest_news': latest_news}, context_instance=RequestContext(request))
    

