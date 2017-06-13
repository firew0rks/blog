from django import forms

class UploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField()
    tags = forms.CharField(required=False)
    article = forms.FileField()
