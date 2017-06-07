from django.forms import forms

class UploadForm(forms.Form):
    article = forms.FileField()