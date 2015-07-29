from django import forms
from models import AMBASSADOR_TYPE_CHOICES, Ambassador

class RegistrationForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    ambassador_nickname = forms.CharField(max_length=20, label="Nickname", error_messages={'required': 'Required. How you will be displayed to other Ambassadors.'})
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_again = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Password (again)")
    code = forms.CharField(max_length=4, min_length=4, label="Choose your Ambassador code", error_messages={'required': 'Your unique four-character Ambassador code you will give people when inviting them to the festival.'})
    target = forms.ChoiceField(choices=AMBASSADOR_TYPE_CHOICES, label="You are")
    phone = forms.CharField(max_length=20)
    referring_ambassador_code = forms.CharField(max_length=4, label="Friend's Ambassador Code")
    ts_and_cs = forms.BooleanField(label="I agree to how the Ambassador Scheme works.", initial=False)
    
    def clean_password_again(self):
        if self.cleaned_data['password_again'] != self.cleaned_data['password']:
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data['password_again']
    
    def clean_email(self):
        if Ambassador.objects.filter(user__email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("E-mail address already registered.")
        return self.cleaned_data['email']
    
    def clean_code(self):
        if Ambassador.objects.filter(code__iexact=self.cleaned_data['code']):
            raise forms.ValidationError("Another Ambassador already has this code; pick another.")
        elif 'NONE' == self.cleaned_data['code']:
            raise forms.ValidationError("Sorry, you must use a proper Ambassador code.")
        return self.cleaned_data['code'].upper()
        
    def clean_referring_ambassador_code(self):
        if not Ambassador.objects.filter(code__iexact=self.cleaned_data['referring_ambassador_code']):
            raise forms.ValidationError("Not a valid Ambassador code")
        elif self.cleaned_data['referring_ambassador_code'].upper() == 'NONE':
            raise forms.ValidationError("Cannot use 'NONE' - must be a valid Ambassador Code")
        return self.cleaned_data['referring_ambassador_code'].upper()
    
    def clean_nickname(self):
        if Ambassador.objects.filter(nickname__iexact=self.cleaned_data['nickname']):
            raise forms.ValidationError("Nickname already in use; pick another")
        return self.cleaned_data['nickname']

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    new_password_again = forms.CharField(max_length=30, widget=forms.PasswordInput, label="New password (again)")
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
    
    def clean_current_password(self):
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError("Your old password was entered incorrectly.  Please enter it again.")
    
    def clean_new_password_again(self):
        if self.cleaned_data['new_password_again'] != self.cleaned_data['new_password']:
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data['new_password_again']

class ClaimSaleForm(forms.Form):
    fname = forms.CharField(label="First name", max_length=20, required=False)
    lname = forms.CharField(label="Last name", max_length=15, required=False)
    email = forms.EmailField(label="Email", required=False)
    phone = forms.CharField(max_length=20, required=False)
    other_details = forms.CharField(widget=forms.Textarea, required=False)
