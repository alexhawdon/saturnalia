from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Artist, ArtistDetailLine
from random import shuffle
from saturnalia.news.models import NewsItem
from forms import ArtistApplication

def artist_detail(request, artist_url):
    artist_name = artist_url.replace('-', ' ')
    artist = Artist.objects.filter(display=True).get(name__iexact=artist_name)
    detail_lines = ArtistDetailLine.objects.filter(artist=artist).order_by('line_number')
    return render_to_response('artist_detail.html',
                              {'artist': artist, 'detail_lines': detail_lines},
                              context_instance=RequestContext(request))
                              
def artistmenu(request):
    artists = list(Artist.objects.filter(display=True))
    shuffle(artists)
    artists.sort(key=lambda artist: artist.promotion_priority)
    
    topSix = []
    count = 0
    while count < 6:
        topSix.append(artists.pop(0))
        count += 1
    
    return render_to_response('artistmenu.html',
            {'artists': artists,
             'topSix': topSix},
             context_instance=RequestContext(request))
    
    return redirect("/")

def artist_application(request):
    latest_news = NewsItem.objects.all()[0]
    if request.method == 'POST':
        form = ArtistApplication(request.POST)
        if form.is_valid():
            artist = Artist(name = form.cleaned_data['name'],
                            description = form.cleaned_data['description'],
                            phone = form.cleaned_data['phone'],
                            website = form.cleaned_data['website'],
                            soundcloud = form.cleaned_data['soundcloud'],
                            facebook = form.cleaned_data['facebook'],
                            myspace = form.cleaned_data['myspace'],
                            lastfm = form.cleaned_data['lastfm'],
                            twitter = form.cleaned_data['twitter'],
                            youtube = form.cleaned_data['youtube'],
                            resident_advisor = form.cleaned_data['resident_advisor'])
            artist.save()
            return redirect('/artists/application-successful/')
    else:
        form = ArtistApplication()
    return render_to_response('artist_application.html',
                              {'form': form,
                               'latest_news': latest_news},
                               context_instance=RequestContext(request))

def application_successful(request):
    latest_news = NewsItem.objects.all()[0]
    return render_to_response('application_successful.html',
                              {'latest_news': latest_news},
                              context_instance=RequestContext(request))
