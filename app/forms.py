from django import forms

class VideoForm(forms.Form):
    url = forms.URLField(label='Video URL')