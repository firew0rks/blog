from django import forms
from markdownx.fields import MarkdownxFormField


class BaseArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField()
    tags = forms.CharField(required=False)


class UploadForm(BaseArticleForm):
    article = forms.FileField()


class CreateForm(BaseArticleForm):
    article = MarkdownxFormField()
