import random
from django.core.files import File
import functions
from saturnalia.settings import PROJECT_PATH
from django.core.files.storage import FileSystemStorage

from django.db import models

upload_storage = FileSystemStorage(location=PROJECT_PATH, base_url='/tickets')

STATE_CHOICES = (
    (u'PP', u'Payment Pending'),
    (u'PD', u'Paid'),
    (u'CN', u'Cancelled')
)

class Order(models.Model):
    #id - Order number PK - AUTOMATICALLY ADDED BY DJANGO
    fname = models.CharField('First name(s)', max_length=20)
    lname = models.CharField('Last name', max_length=15)
    email = models.EmailField('Email address')
    phone = models.CharField('Phone number', max_length=20)
    state = models.CharField('Order Status', 
                              max_length=2,
                              choices=STATE_CHOICES,
                              default=u'PP')
    
    def __unicode__(self):
        return str(self.id) + ": " + self.fname + " " + self.lname + " " + self.state
        
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        #Create a related OrderState instance recording the time and state
        state = OrderState(order=self, state=self.state)
        state.save()
   
    
class Deposit(models.Model):
    code = models.IntegerField('Unique deposit number', primary_key=True, editable=False)
    order = models.ForeignKey('Order')
    ambassador = models.ForeignKey('ambassadors.Ambassador') #Ambassador responsible for the sale
    ticket = models.ImageField(upload_to="tickets/", blank=True, storage=upload_storage)
    
    def __unicode__(self):
            return str(self.code) + ": " + str(self.order)
                
    def save(self, *args, **kwargs):
        #Generate unique and random 6-digit deposit code if not already done
        if not self.code:
            self.code = random.randint(100000, 999999)
            while Deposit.objects.filter(code=self.code) or Ticket.objects.filter(code=self.code):
                self.code = random.randint(100000, 999999)
        super(Deposit, self).save(*args, **kwargs)

class Balance(models.Model):
    #id - PK - AUTOMATICALLY ADDED BY DJANGO
    order = models.ForeignKey('order')
    deposit = models.ForeignKey('Deposit',
                                #Can only pay balance if deposit is paid!
                                limit_choices_to = {'order__state__exact': 'PD'})
    
    def __unicode__(self):
        return str(self.deposit.code) + self.order.state
    
class Ticket(models.Model):
    code = models.IntegerField('Unique ticket number', primary_key=True, editable=False)
    order = models.ForeignKey('Order')
    ambassador = models.ForeignKey('ambassadors.Ambassador')
    ticket = models.ImageField(upload_to="tickets/", storage=upload_storage, blank=True)
    
    def __unicode__(self):
        return str(self.code)
        
    def save(self, *args, **kwargs):
        #Generate unique 6-digit ticket code if not already done
        if not self.code:
            self.code = random.randint(100000, 999999)
            while Ticket.objects.filter(code=self.code) or Deposit.objects.filter(code=self.code):
                self.code = random.randint(100000, 999999)
        super(Ticket, self).save(*args, **kwargs)

class OrderState(models.Model):
    #id - PK - AUTOMATICALLY ADDED BY DJANGO
    order = models.ForeignKey('Order')
    state = models.CharField('Order Status', max_length=2, choices=STATE_CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time']
    
    def __unicode__(self):
        return str(self.id) + ": Order: " + str(self.order.id) + ", State: " + self.state + ", Time: " + str(self.time)
