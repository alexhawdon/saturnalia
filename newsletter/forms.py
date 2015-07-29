from django import forms

class NewsletterForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    def clean_name(self):
        if self.cleaned_data['name'] == 'Full Name':
            raise forms.ValidationError("You're NOT called 'Full Name'")
        return self.cleaned_data['name']
