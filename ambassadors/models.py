from django.db import models
from django.contrib.auth.models import User
from saturnalia.shop.models import Balance, Ticket, Deposit, OrderState

AMBASSADOR_TYPE_CHOICES=((10, u'an Ambassador'),
                         (3, u'a Solo Contributor (Performer/Artist/DJ/Volunteer)'),
                         (6, u'a Band')
                        )

class AmbassadorManager(models.Manager):
    def top10(self):
        top10 = []
        #Create list of ambassador name and score dictionaries
        for ambassador in Ambassador.objects.filter(user__is_active=True).exclude(code='NONE'):
            top10.append({'nickname': ambassador.nickname,
                          'score': len(ambassador.sales()),
                          'deposits': len(ambassador.deposits())})
        #sort on name
        top10.sort(key=lambda ambassador: ambassador['nickname'])
        #Then deposits
        top10.sort(key=lambda ambassador: ambassador['deposits'], reverse=True)
        #Then by score
        top10.sort(key=lambda ambassador: ambassador['score'], reverse=True)
        return top10[:10]

class Ambassador(models.Model):
    code = models.CharField('Unique ambassador code', max_length=4, unique=True)
    target = models.SmallIntegerField('Ambassador type', 
                                      choices=AMBASSADOR_TYPE_CHOICES)
    phone = models.CharField('Phone number', max_length=20)
    paid_deposit = models.OneToOneField('shop.Deposit', #Ambassador must have bought a deposit 
                                   limit_choices_to={'order__state__exact': 'PD'},
                                   related_name='paid_deposit',
                                   null=True, blank = True)
    nickname = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User)
    
    objects = AmbassadorManager()
    
    def __unicode__(self):
        return self.code + ": " + self.user.email
        
    def sales(self):
        """Returns list of this ambassador's sales - one dictionary object for each"""
        
        sales = []
        #Add each balance related to a paid order and related to a paid (implied
        #in model restriction on relationship) despoit which is attributed to 
        #this ambassador
        for balance in Balance.objects.filter(order__state='PD').filter(deposit__ambassador__code__iexact=self.code):
            sales.append({'name': balance.order.fname + " " + balance.order.lname,
                          'date': OrderState.objects.order_by('-time').filter(order__id=balance.order.id)[0].time})
        #Add each ticket related to a paid order and related to this ambassador
        for ticket in Ticket.objects.filter(order__state='PD').filter(ambassador__code__iexact=self.code):
            sales.append({'name': ticket.order.fname + " " + ticket.order.lname,
                          'date': OrderState.objects.order_by('-time').filter(order__id=ticket.order.id)[0].time})
        #Sort the list for viewing consistency
        sales.sort(key=lambda sale: sale['date'])
        return sales
    
    def num_sales(self):
        return len(self.sales())
    
    def sales_remaining(self):
        return self.target - self.num_sales()
    
    def deposits(self):
        """List of ambassador's deposits - one dictionary object each"""
        deposits = []
        #First get list of paid deposits related to this ambassador
        for deposit in Deposit.objects.filter(order__state='PD').filter(ambassador__code__iexact=self.code):
            #then test that each one isn't related to a balance related to balance related to a paid order
            if not Balance.objects.filter(deposit__code=deposit.code).filter(order__state='PD'):
                deposits.append({'name': deposit.order.fname + " " + deposit.order.lname,
                                 'code': deposit.code,
                                 'date': OrderState.objects.order_by('-time').filter(order__id=deposit.order.id)[0].time})
        #Sort the list for viewing consistency
        deposits.sort(key=lambda deposit: deposit['date'])
        return deposits

class SaleClaim(models.Model):
    #id - Order number PK - AUTOMATICALLY ADDED BY DJANGO
    ambassador = models.ForeignKey(Ambassador)
    date = models.DateTimeField(auto_now_add=True)
    fname = models.CharField('First name(s)', max_length=20, blank=True)
    lname = models.CharField('Last name', max_length=15, blank=True)
    email = models.EmailField('Email address', blank=True)
    phone = models.CharField('Phone number', max_length=20, blank=True)
    other_details = models.TextField(blank=True)
    processed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.ambassador.nickname
