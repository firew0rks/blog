import datetime
import logging
import os

import markdown
import re
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView

from blog.wiki.forms import UploadForm, CreateForm
from blog.wiki.models import Article, Tag

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
        toc = md.toc

        print(toc)
        # Render toc nicely using bootstrap

        return render(request, 'wiki/article.html', {'text': html, 'toc': toc})


class SearchView(ListView):
    template_name = 'wiki/search.html'
    paginate_by = 10
    context_object_name = 'article_list'

    def get(self, *args, **kwargs):
        keywords = self.request.GET.get('search')
        # TODO: Multiple keyword searches

        self.queryset = Article.objects.filter(
            Q(url__icontains=keywords) |
            Q(title__icontains=keywords) |
            Q(tags__tag__icontains=keywords)
        ).distinct()

        return super(SearchView, self).get(*args, **kwargs)


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
        # TODO: Implement tags for upload view

        # Obtaining the uploaded file
        file = self.request.FILES['article']

        tmp_path = os.path.join(os.path.dirname(__file__), 'article/%s.md' % a.url)
        with open(tmp_path, 'w+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        a.location = ('article/%s.md' % a.url)
        a.save(version=1)

        return super(UploadView, self).form_valid(form)


class CreateView(FormView):
    # TODO: Implement ajax-based save & continue
    template_name = 'wiki/create.html'
    form_class = CreateForm
    success_url = '/wiki/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        # Grabbing all the tag values
        tags = [value for name, value in request.POST.iteritems() if name.startswith('n_')]

        if form.is_valid():
            return self.form_valid2(form, tags)
        else:
            return self.form_invalid(form)

    def form_valid2(self, form, tags):
        a = Article()

        a.author = self.request.user
        a.created = datetime.datetime.now()
        a.modified = datetime.datetime.now()

        a.title = form.cleaned_data['title']
        a.url = form.cleaned_data['slug']

        # String containing the wiki article
        article = form.cleaned_data['article']

        tmp_path = os.path.join(os.path.dirname(__file__), 'article/%s.md' % a.url)
        # TODO: Write a parser that saves title information, and preview text (first 200 characters)
        with open(tmp_path, 'w+') as f:
            f.write(article)

        a.location = ('article/%s.md' % a.url)

        # Generating preview text from text between <p>...</p> elements
        html = markdown.markdown(article)
        text = re.findall('<p>(.+)</p>', html)
        text = ' '.join(text)
        a.preview_text = text[:200] + '...'

        # Saving reference of article to database
        a.save(version=1)

        # Associating tags with the article
        for t in tags:
            try:
                tt = Tag.objects.get(tag__iexact=t)
            except ObjectDoesNotExist:
                tt = Tag(tag=t)
                tt.save()

            a.tags.add(tt)

        a.save(version=1)

        # Redirects user to success url
        messages.success(self.request, 'New Article Created!')
        return self.form_valid(form)

