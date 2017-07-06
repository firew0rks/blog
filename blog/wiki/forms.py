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


class EditForm(CreateForm):
    def clean_slug(self):
        if self.instance.slug != self.cleaned_data['slug']:
            raise forms.ValidationError("The slug field cannot be changed in edit mode")
