from django import forms

class RecommendationForm(forms.Form):
    artist_name = forms.CharField(max_length=100)
    genres = forms.CharField(max_length=100)
    attrs = forms.CharField(max_length=100)