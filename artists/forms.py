from django import forms

class ArtistApplication(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)
    website = forms.URLField(required=False)
    facebook = forms.URLField(required=False)
    myspace = forms.URLField(required=False)
    soundcloud = forms.URLField(required=False)
    lastfm = forms.URLField(required=False)
    twitter = forms.URLField(required=False)
    youtube = forms.URLField(required=False)
    resident_advisor = forms.URLField(required=False)
