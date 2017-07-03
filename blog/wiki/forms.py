from django import forms
from markdownx.fields import MarkdownxFormField


class BaseArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(help_text="*This field will automatically fill in once you've entered a title")
    tags = forms.CharField(required=False)


class UploadForm(BaseArticleForm):
    article = forms.FileField()


class CreateForm(BaseArticleForm):
    article = MarkdownxFormField()
