from django.contrib import admin

from models import Order, Deposit, Balance, Ticket, OrderState

admin.site.register(Order)
admin.site.register(Deposit)
admin.site.register(Balance)
admin.site.register(Ticket)
admin.site.register(OrderState)
