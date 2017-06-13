import datetime
import os

import markdown
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import TemplateView, CreateView, FormView, ListView

from blog.wiki.forms import UploadForm
from blog.wiki.models import Article

logger = logging.getLogger('django.request')


def home(request):
    return render(request, 'wiki/home.html')


def article_view(request, slug):
    """
    Renders the markdown article into HTML and displays it
    """
    try:
        a = Article.objects.get(url=slug)
    except:
        # Article does not exist
        HttpResponseRedirect(reverse('article_invalid'))

    path = os.path.join(os.path.dirname(__file__), a.location)
    with open(path, 'rU') as f:
        text_string = f.read()
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        html = md.convert(text_string)

        # TODO: Render toc nicely without bullet points
        return render(request, 'wiki/article.html', {'text': html, 'toc': md.toc})


class ArticleSearch(ListView):
    template_name = 'wiki/search.html'
    paginate_by = 10
    context_object_name = 'article_list'

    def get(self, *args, **kwargs):
        keywords = self.request.GET.get('search')
        self.queryset = Article.objects.filter(url__contains=keywords)
        print(self.queryset.__len__())
        return super(ArticleSearch, self).get(*args, **kwargs)


class UploadView(FormView):
    template_name = 'wiki/upload.html'
    form_class = UploadForm
    success_url = '/wiki/'
    success_message = 'Successfully uploaded markdown document'

    # Form valid occurs after is_valid is checked in a post request
    def form_valid(self, form):
        """
        Overriding form_valid method to save files to a particular location
        """

        # Filling out information for the article
        a = Article()
        a.author = self.request.user
        a.date_created = datetime.datetime.now()
        a.date_modified = datetime.datetime.now()

        # Filling out information from form
        a.title = form.cleaned_data['title']
        a.url = form.cleaned_data['slug']
        # TODO: Tags

        # Obtaining the uploaded file
        file = self.request.FILES['article']

        tmp_path = os.path.join(os.path.dirname(__file__), 'article/%s.md' % a.url)
        with open(tmp_path, 'w+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        a.location = 'article/%s.md' % a.url
        a.save(version=1)

        return super(UploadView, self).form_valid(form)


