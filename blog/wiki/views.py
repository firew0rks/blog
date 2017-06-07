import markdown
import logging

from django.shortcuts import render

from django.views.generic import TemplateView

logger = logging.getLogger('django.request')


def home(request):
    return render(request, 'wiki/home.html')


def article_view(request):
    with open('Django Notes.md', 'rU') as f:
        text_string = f.read()
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        html = md.convert(text_string)

        # TODO: Render toc nicely without bullet points
        return render(request, 'wiki/article.html', {'text': html, 'toc': md.toc})


class UploadView(TemplateView):
