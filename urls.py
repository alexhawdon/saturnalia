import os
from django.conf.urls.defaults import *
from django.conf import settings

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^v2/', include('v2.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    #Ambassador 
    (r'^ambassador/$', 'saturnalia.ambassadors.views.about'),
    (r'^ambassador/register/$', 'saturnalia.ambassadors.views.register'),
    (r'^ambassador/registration_successful/$', 'saturnalia.ambassadors.views.registration_successful'),
    (r'^ambassador/dashboard/$', 'saturnalia.ambassadors.views.dashboard'),
    (r'^ambassador/claim-sale/$', 'saturnalia.ambassadors.views.claim_sale'),
    (r'^ambassador/claim-registered/$', 'saturnalia.ambassadors.views.claim_registered'),
    (r'^ambassador/change-password/$', 'saturnalia.ambassadors.views.change_password'),
    (r'^ambassador/password-change-successful', 'saturnalia.ambassadors.views.password_change_successful'),
    
    #Static Pages
    (r'^$', 'saturnalia.views.home'),
    (r'^about/$', 'saturnalia.views.about'),
    (r'^social-media/$', 'saturnalia.views.social_media'),
    (r'^terms-and-conditions/$', 'saturnalia.views.terms_and_conditions'),
    
    #Login handling
    (r'^login/$', 'saturnalia.views.login'),
    (r'^logout/$', 'saturnalia.views.logout'),
    (r'^forgotten-password/$', 'saturnalia.views.forgotten_password'),
    (r'^reset-sent/$', 'saturnalia.views.reset_sent'),
    (r'^login-required/$', 'saturnalia.views.login_required'),
    
    #Shop
    (r'^tickets/$', 'saturnalia.shop.views.tickets'),
    (r'^tickets/process_order/$', 'saturnalia.shop.views.process_order'),
    (r'^tickets/pay-balance/$', 'saturnalia.shop.views.pay_balance'),
    (r'^tickets/find-paid-order/$', 'saturnalia.shop.views.find_paid_order'),
    (r'^tickets/change-order-state/$', 'saturnalia.shop.views.change_order_state'),
    (r'^tickets/retrieve/$', 'saturnalia.shop.views.retrieve'),
    (r'^tickets/retrieved/$', 'saturnalia.shop.views.retrieved'),
    
    #artists
    (r'^artists/$', 'saturnalia.artists.views.artistmenu'),
    (r'^artists/apply/$', 'saturnalia.artists.views.artist_application'),
    (r'^artists/application-successful/$', 'saturnalia.artists.views.application_successful'),
    (r'^artists/([^/]+)/', 'saturnalia.artists.views.artist_detail'),
    
    #News
    (r'^news/$', 'saturnalia.news.views.news_items'),
    (r'^news/page/(?P<page>\d{1,2})/$', 'saturnalia.news.views.news_items'),
    (r'^news/tag/(?P<category>[^/]+)/$', 'saturnalia.news.views.news_items'),
    (r'^news/tag/(?P<category>[^/]+)/page/(?P<page>\d{1,2})/$', 'saturnalia.news.views.news_items'),
    (r'^news/view/(\d{1,3})/$', 'saturnalia.news.views.news_item_detail'),
    
    #What's on
    (r'^whats-on/$', 'saturnalia.views.whats_on'),
    (r'^whats-on/arenas/$', 'saturnalia.views.arenas'),
    (r'^whats-on/art/$', 'saturnalia.views.art'),
    (r'^whats-on/activities/$', 'saturnalia.views.activities'),
    (r'^whats-on/ameneties/$', 'saturnalia.views.ameneties'),
    (r'^whats-on/film/$', 'saturnalia.views.film'),
    
    #Newsletter
    (r'^newsletter/$', 'saturnalia.newsletter.views.newsletter'),
    (r'^newsletter/signup-successful/', 'saturnalia.newsletter.views.signup_successful'),
    
    #Contact
    (r'^contact/thanks/', 'saturnalia.contact.views.thanks'),
    (r'^contact/', 'saturnalia.contact.views.contact'),
    
    #FAQ
    (r'^faq/$', 'saturnalia.faq.views.faq'),
)
