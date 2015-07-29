# -*- coding: utf-8 -*- 
from django import forms
from saturnalia.ambassadors.models import Ambassador
from models import Deposit, Balance

QUANTITY_CHOICES=((0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10))

class BaseOrderForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    phone = forms.CharField(max_length=20)
    
class TicketDepositOrderForm(BaseOrderForm):
    tickets = forms.ChoiceField(choices=QUANTITY_CHOICES, label="Tickets @ £55 + 2.50 booking fee") #TODO: Upgrade this to a spinner
    deposits = forms.ChoiceField(choices=QUANTITY_CHOICES, label="Deposits @ £5.50 + 2.50 booking fee*") #TODO: Upgrade this to a spinner
    referring_ambassador_code = forms.CharField(min_length=4, max_length=4, 
                                                error_messages={'required': 'If a Summer Saturnalia Ambassador gave you their code enter it here.  If not, enter "NONE"'},
                                                label="Ambassador Code")
    ts_and_cs = forms.BooleanField(label='I agree to the terms and conditions of sale (below).', initial=False)
    
    def clean_referring_ambassador_code(self):
        if not Ambassador.objects.filter(code__iexact=self.cleaned_data['referring_ambassador_code'].upper()):
            raise forms.ValidationError("Enter a valid Ambassador code.  If you do not have one, enter 'NONE'.")
        return self.cleaned_data['referring_ambassador_code'].upper()
        
    def clean(self):
        if self.cleaned_data.get('tickets') == "0" and self.cleaned_data.get('deposits') == "0":
            raise forms.ValidationError("Please select a quantity of tickets and/or deposits to purchase.")
        return self.cleaned_data

class BalanceOrderForm(BaseOrderForm):
    deposit_code_one = forms.IntegerField(label="Deposit code 1", min_value=100000, max_value=999999)
    deposit_code_two = forms.IntegerField(label="Deposit code 2", required = False, min_value=100000, max_value=999999)
    deposit_code_three = forms.IntegerField(label="Deposit code 3", required=False, min_value=100000, max_value=999999)
    deposit_code_four = forms.IntegerField(label="Deposit code 4", required=False, min_value=100000, max_value=999999)
    deposit_code_five = forms.IntegerField(label="Deposit code 5", required=False, min_value=100000, max_value=999999)
    ts_and_cs = forms.BooleanField(label='I agree to the terms and conditions of sale.', initial=False)
    
    def clean_deposit_code_one(self):
        if self.cleaned_data['deposit_code_one']:
            code = self.cleaned_data['deposit_code_one']
            if Deposit.objects.filter(code=code).filter(order__state='PP'):
                raise forms.ValidationError("Deposit code valid but payment is still processing.  Payment may take up to a day to be reflected here.")
            elif Balance.objects.filter(deposit__code=code):
                raise forms.ValidationError("Someone has already paid the balance for this deposit.  If this wasn't you, you'd better get in touch.")
            elif not Deposit.objects.filter(code=code).filter(order__state='PD'):
                raise forms.ValidationError("Not a valid deposit code - check and re-enter.")
            return code
    
    def clean_deposit_code_two(self):
        if self.cleaned_data['deposit_code_two']:
            code = self.cleaned_data['deposit_code_two']
            if Deposit.objects.filter(code=code).filter(order__state='PP'):
                raise forms.ValidationError("Deposit code valid but payment is still processing.  Successful Google Checkout payment may take up to a day to be reflected here.")
            elif Balance.objects.filter(deposit__code=code):
                raise forms.ValidationError("Someone has already paid the balance for this deposit.  If this wasn't you, you'd better get in touch.")
            elif not Deposit.objects.filter(code=code).filter(order__state='PD'):
                raise forms.ValidationError("Not a valid deposit code - check and re-enter.")
            return code
    
    def clean_deposit_code_three(self):
        if self.cleaned_data['deposit_code_three']:
            code = self.cleaned_data['deposit_code_three']
            if Deposit.objects.filter(code=code).filter(order__state='PP'):
                raise forms.ValidationError("Deposit code valid but payment is still processing.  Successful Google Checkout payment may take up to a day to be reflected here.")
            elif Balance.objects.filter(deposit__code=code):
                raise forms.ValidationError("Someone has already paid the balance for this deposit.  If this wasn't you, you'd better get in touch.")
            elif not Deposit.objects.filter(code=code).filter(order__state='PD'):
                raise forms.ValidationError("Not a valid deposit code - check and re-enter.")
            return code
    
    def clean_deposit_code_four(self):
        if self.cleaned_data['deposit_code_four']:
            code = self.cleaned_data['deposit_code_four']
            if Deposit.objects.filter(code=code).filter(order__state='PP'):
                raise forms.ValidationError("Deposit code valid but payment is still processing.  Successful Google Checkout payment may take up to a day to be reflected here.")
            elif Balance.objects.filter(deposit__code=code):
                raise forms.ValidationError("Someone has already paid the balance for this deposit.  If this wasn't you, you'd better get in touch.")
            elif not Deposit.objects.filter(code=code).filter(order__state='PD'):
                raise forms.ValidationError("Not a valid deposit code - check and re-enter.")
            return code
    
    def clean_deposit_code_five(self):
        if self.cleaned_data['deposit_code_five']:
            code = self.cleaned_data['deposit_code_five']
            if Deposit.objects.filter(code=code).filter(order__state='PP'):
                raise forms.ValidationError("Deposit code valid but payment is still processing.  Successful Google Checkout payment may take up to a day to be reflected here.")
            elif Balance.objects.filter(deposit__code=code):
                raise forms.ValidationError("Someone has already paid the balance for this deposit.  If this wasn't you, you'd better get in touch.")
            elif not Deposit.objects.filter(code=code).filter(order__state='PD'):
                raise forms.ValidationError("Not a valid deposit code - check and re-enter.")
            return code
