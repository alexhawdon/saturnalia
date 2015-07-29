# -*- coding: utf-8 -*- 
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from forms import TicketDepositOrderForm, BalanceOrderForm
from saturnalia.ambassadors.models import Ambassador
from models import Order, Deposit, Balance, Ticket
from httplib2 import Http
from urllib import urlencode
from saturnalia.news.models import NewsItem
import functions

def tickets(request):
    latest_news = NewsItem.objects.all()[0]
    if (('tickets' in request.GET and request.GET['tickets']) or 
       ('deposits' in request.GET and request.GET['deposits']) or
       ('first_name' in request.GET and request.GET['first_name']) or
       ('last_name' in request.GET and request.GET['last_name']) or
       ('email' in request.GET and request.GET['email']) or
       ('phone' in request.GET and request.GET['phone']) or
       ('referring_ambassador_code' in request.GET and request.GET['referring_ambassador_code'])):
        form = TicketDepositOrderForm(request.GET)
        if form.is_valid():
            tickets = form.cleaned_data['tickets']
            deposits = form.cleaned_data['deposits']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            referring_ambassador_code = form.cleaned_data['referring_ambassador_code']
            return render_to_response('confirm_order.html',
                                      {'tickets': tickets,
                                       'deposits': deposits,
                                       'first_name': first_name,
                                       'last_name': last_name,
                                       'email': email,
                                       'phone': phone,
                                       'referring_ambassador_code': referring_ambassador_code,
                                       'latest_news': latest_news},
                                      context_instance=RequestContext(request))
    else:
        form = TicketDepositOrderForm()
    return render_to_response('tickets.html',
                              {'form': form,
                               'latest_news': latest_news},
                              context_instance=RequestContext(request))

def pay_balance(request):
    latest_news = NewsItem.objects.all()[0]
    if (('deposit_code_one' in request.GET and request.GET['deposit_code_one']) or 
       ('deposit_code_two' in request.GET and request.GET['deposit_code_two']) or
       ('deposit_code_three' in request.GET and request.GET['deposit_code_three']) or
       ('deposit_code_four' in request.GET and request.GET['deposit_code_four']) or
       ('deposit_code_five' in request.GET and request.GET['deposit_code_five']) or
       ('first_name' in request.GET and request.GET['first_name']) or
       ('last_name' in request.GET and request.GET['last_name']) or
       ('email' in request.GET and request.GET['email']) or
       ('phone' in request.GET and request.GET['phone'])):
        #User has submitted the form
        form = BalanceOrderForm(request.GET)
        if form.is_valid():
            #Show them the order confirmation page
            return render_to_response('confirm_order.html',
                                      {'deposit_code_one': form.cleaned_data['deposit_code_one'],
                                       'deposit_code_two': form.cleaned_data['deposit_code_two'],
                                       'deposit_code_three': form.cleaned_data['deposit_code_three'],
                                       'deposit_code_four': form.cleaned_data['deposit_code_four'],
                                       'deposit_code_five': form.cleaned_data['deposit_code_five'],
                                       'first_name': form.cleaned_data['first_name'],
                                       'last_name': form.cleaned_data['last_name'],
                                       'email': form.cleaned_data['email'],
                                       'phone': form.cleaned_data['phone'],
                                       'latest_news': latest_news},
                                      context_instance=RequestContext(request))
    else: #no form submission - give them the blank one
        form = BalanceOrderForm()
    return render_to_response('pay_balance.html',
                              {'form': form,
                               'latest_news': latest_news},
                              context_instance=RequestContext(request))

def process_order(request):
    if request.method == 'POST':
        #Pull all data out of POST (some of it mightn't  be there)
        if request.POST.get('tickets'):
            tickets = int(request.POST.get('tickets', ''))
        if request.POST.get('deposits', ''):
            deposits = int(request.POST.get('deposits', ''))
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        referring_ambassador_code = request.POST.get('referring_ambassador_code', '')
        deposit_code_one = request.POST.get('deposit_code_one', '')
        deposit_code_two = request.POST.get('deposit_code_two', '')
        deposit_code_three = request.POST.get('deposit_code_three', '')
        deposit_code_four = request.POST.get('deposit_code_four', '')
        deposit_code_five = request.POST.get('deposit_code_five', '')
        
        #First build the order
        order = Order(fname=first_name,
                      lname=last_name,
                      email=email,
                      phone=phone)
        order.save()
        
        #Initialise the lists to hold the possible ordered items
        ordered_tickets = []
        ordered_deposits = []
        ordered_balances = []
        
        
        if referring_ambassador_code: #Purchasing tickets and/or deposits
            referring_ambassador = Ambassador.objects.get(code=referring_ambassador_code)
            
            #Then generate tickets and deposits
            while tickets > 0:
                ticket = Ticket(order=order, ambassador=referring_ambassador)
                ticket.save()
                ordered_tickets.append(ticket)
                tickets -= 1
            
            while deposits > 0:
                deposit = Deposit(order=order, ambassador=referring_ambassador)
                deposit.save()
                ordered_deposits.append(deposit)
                deposits -= 1
        
        else: #Purchasing balances for paid deposits 
            if deposit_code_one != 'None':
                balance = Balance(order=order, deposit=Deposit.objects.get(code=deposit_code_one))
                balance.save()
                ordered_balances.append(balance)
            if deposit_code_two != 'None':
                balance = Balance(order=order, deposit=Deposit.objects.get(code=deposit_code_two))
                balance.save()
                ordered_balances.append(balance)
            if deposit_code_three != 'None':
                balance = Balance(order=order, deposit=Deposit.objects.get(code=deposit_code_three))
                balance.save()
                ordered_balances.append(balance)
            if deposit_code_four != 'None':
                balance = Balance(order=order, deposit=Deposit.objects.get(code=deposit_code_four))
                balance.save()
                ordered_balances.append(balance)
            if deposit_code_five != 'None':
                balance = Balance(order=order, deposit=Deposit.objects.get(code=deposit_code_five))
                balance.save()
                ordered_balances.append(balance)
            
        #Build the XML request for Google Checkout
        data = {"_type": "checkout-shopping-cart",
                "_charset_":""}
        itemcount = 0
        for ticket in ordered_tickets:
            itemcount += 1
            data['item_name_'+ str(itemcount)] = "1 x Summer Saturnalia 2011 Ticket"
            data['item_description_'+str(itemcount)] = 'One ticket including £2.50 booking fee. Unique ticket code: ' + str(ticket.code)
            data['item_price_'+str(itemcount)] = "57.50"
            data['item_currency_'+str(itemcount)] = "GBP"
            data['item_quantity_'+str(itemcount)] = "1"
            data['item_merchant_id_'+str(itemcount)] = ticket.code
            data['shopping-cart.items.item-'+str(itemcount)+'.digital-content.display-disposition'] = "OPTIMISTIC"
            data['shopping-cart.items.item-'+str(itemcount)+'.digital-content.description'] = "After your payment has been processed your printable ticket will be emailed to you; this normally takes less than a day."
        
        for deposit in ordered_deposits:
            itemcount += 1
            data['item_name_'+str(itemcount)] = "1 x Summer Saturnalia 2011 Deposit"
            data['item_description_'+str(itemcount)] = "One deposit including £2.50 booking fee. Unique deposit code: " + str(deposit.code)
            data['item_price_'+str(itemcount)] = "8"
            data['item_currency_'+str(itemcount)] = "GBP"
            data['item_quantity_'+str(itemcount)] = "1"
            data['item_merchant_id_'+str(itemcount)] = deposit.code
            data['shopping-cart.items.item-'+str(itemcount)+'.digital-content.display-disposition'] = "OPTIMISTIC"
            data['shopping-cart.items.item-'+str(itemcount)+'.digital-content.description'] = "Your deposit code is " + str(deposit.code) +".  You can use this code to pay the balance and obtain your ticket when payment has been processed.  This normally takes less than a day, after which a copy of this code will be emailed to you. "
        
        for balance in ordered_balances:
            itemcount += 1
            data['item_name_'+str(itemcount)] = "1 x Summer Saturnalia 2011 Balance Payment (Ticket)"
            data['item_description_'+str(itemcount)] = "The final payment for deposit number " + str(balance.deposit.code) + " - Booking already included in deposit."
            data['item_price_'+str(itemcount)] = "49.50"
            data['item_currency_'+str(itemcount)] = "GBP"
            data['item_quantity_'+str(itemcount)] = "1"
            data['item_merchant_id_'+str(itemcount)] = balance.deposit.code
            data['shopping-cart.items.item-'+str(itemcount)+'.digital-content.display-disposition'] = "OPTIMISTIC"
            data['shopping-cart.items.item-'+str(itemcount)+'.digital-content.description'] = "After your payment has been processed your printable ticket will be emailed to you; this normally takes less than a day."
        
        #Build the rest of the request and send to Google
        headers = {"Content-Type": 'application/xml; charset=UTF-8',
                   "Accpt": 'application/xml; charset=UTF-8'}

        h = Http()
        h.add_credentials('210280845590798', 'qqnL2K9V76aNWEVVXAoLtQ')

        resp, content = h.request("https://checkout.google.com/api/checkout/v2/checkoutForm/Merchant/210280845590798", 
                                  "POST",
                                  urlencode(data),
                                  headers=headers)
        #If everything worked, we can redirect the user to Google Checkout to complete payment
        
        location = resp['location']
        return redirect(location)
        
def find_paid_order(request):
    if not request.user.is_staff:
        return redirect('/login-required')
    ticket_code = request.GET.get('ticket_code', '')
    deposit_code = request.GET.get('deposit_code', '')
    balance_code = request.GET.get('balance_code', '')
    order = ""
    
    if ticket_code:
        try:
            order = Ticket.objects.get(code=ticket_code).order
        except:
            return render_to_response('find_paid_order.html',
                               {'error': 'No ticket found for code ' +ticket_code},
                               context_instance=RequestContext(request))
    elif deposit_code:
        try:
            order = Deposit.objects.get(code=deposit_code).order
        except:
            return render_to_response('find_paid_order.html',
                               {'error': 'No deposit found for code ' +deposit_code},
                               context_instance=RequestContext(request))
    elif balance_code:
        try:
            order = Balance.objects.get(deposit__code=balance_code).order
        except:
            return render_to_response('find_paid_order.html',
                               {'error': 'No balance found for code ' +balance_code},
                               context_instance=RequestContext(request))
    if order:
        return render_to_response('find_paid_order.html',
                           {'order': order},
                           context_instance=RequestContext(request))
    else:
        return render_to_response('find_paid_order.html',
                           context_instance=RequestContext(request))

def change_order_state(request):
    if request.user.is_staff and request.POST['order']:
        order = Order.objects.get(id=request.POST['order'])
        order.state="PD"
        
        #Start off the email
        mail_msg = '''Dear %s %s,
Thank you for your custom.  Your payment has been processed and we are pleased to digitally deliver the following items:

''' %(order.fname, order.lname)
        attachments=[]
        
        #get items associated with order (tickets, un-completed deposits and paid deposits)
        tickets = Ticket.objects.filter(order=order)
        deposits = Deposit.objects.filter(order=order)
        balances = Balance.objects.filter(order=order)
        
        for ticket in tickets:
            if not ticket.ticket:
                functions.make_ticket(ticket)
            mail_msg += "1 x Summer Saturnalia 2011 E-Ticket, code: %i - attached.\r\n" %ticket.code
            attachments.append(('Ticket'+str(ticket.code)+'.png', ticket.ticket.file.read(), 'image/png'))
        
        for deposit in deposits:
            if not deposit.ticket:
                functions.make_ticket(deposit)
            mail_msg += "1 x Summer Saturnalia 2011 Desposit, DESPOSIT CODE: %i .\r\n" %deposit.code
        
        for balance in balances:
            mail_msg += "1 x Summer Saturnalia 2011 E-Ticket, code: %i - attached.\r\n" %balance.deposit.code
            attachments.append(('Ticket'+str(balance.deposit.code)+'.png', balance.deposit.ticket.file.read(), 'image/png'))
        
        email = EmailMessage(subject="Your E-Tickets or Deposits",
                             body=mail_msg,
                             from_email="Summer Saturnalia <enquiries@summersaturnalia.com>",
                             to=[order.email],
                             attachments=attachments)
        email.send()
        order.save()
        return render_to_response('state_change_successful.html', context_instance=RequestContext(request))

def retrieve(request):
    latest_news = NewsItem.objects.all()[0]
    if request.method == 'POST':
        email = request.POST['email'].strip()
        #Get all paid orders relating to this account
        orders = Order.objects.filter(email=email).filter(state='PD')
        if orders:
            deposits=[]
            tickets=[]
            balances=[]
            for order in orders:
                #Get all deposits related to this order but NOT those for which a balance has been paid.
                for deposit in Deposit.objects.filter(order=order):
                    if not Balance.objects.filter(deposit=deposit):
                        deposits.append(deposit)
                #Get all balances related to this order
                balances += Balance.objects.filter(order=order)
                #Get all tickets related to this order
                tickets += Ticket.objects.filter(order=order)
            
            #Email them all to the user
            mail_msg = '''Dear %s %s,
The following items were previously bought in connection with this email address:

''' %(order.fname, order.lname)
            attachments=[]
            
            for ticket in tickets:
                mail_msg += "1 x Summer Saturnalia 2011 Printable E-Ticket, code: %i - attached." %ticket.code
                attachments.append(('Ticket'+str(ticket.code)+'.png', ticket.ticket.file.read(), 'image/png'))
            
            for deposit in deposits:
                mail_msg += "1 x Summer Saturnalia 2011 Desposit, DESPOSIT CODE: %i ." %deposit.code
            
            for balance in balances:
                mail_msg += "1 x Summer Saturnalia 2011 Printable E-Ticket, code: %i - attached." %balance.deposit.code
                attachments.append(('Ticket'+str(balance.deposit.code)+'.png', balance.deposit.ticket.file.read(), 'image/png'))
            
            email = EmailMessage(subject="Your E-Tickets or Deposits",
                                 body=mail_msg,
                                 from_email="Summer Saturnalia <enquiries@summersaturnalia.com>",
                                 to=[order.email],
                                 attachments=attachments)
            email.send()
            return redirect('/tickets/retrieved/')
        else:
            #No orders in state paid for this email
            return render_to_response('retrieve.html',
                               {'error': 'error',
                                'latest_news': latest_news},
                               context_instance=RequestContext(request))
    else:
        return render_to_response('retrieve.html',
                            {'latest_news': latest_news},
                           context_instance=RequestContext(request))
                           
def retrieved(request):
    return render_to_response('retrieved.html', context_instance=RequestContext(request))
