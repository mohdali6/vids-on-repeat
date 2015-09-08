from django import forms

class VideoSearchForm(forms.Form):
    search_query = forms.CharField(label='Search')