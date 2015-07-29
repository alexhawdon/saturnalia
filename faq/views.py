from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from saturnalia.news.models import NewsItem
from models import Section, QAPair

def faq(request):
    latest_news = NewsItem.objects.all()[0]
    sections = Section.objects.all()
    qapairs = QAPair.objects.all()
    return render_to_response('faq.html',
                              {'latest_news': latest_news,
                               'sections': sections,
                               'qapairs': qapairs},
                               context_instance=RequestContext(request))
