import markdown

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'wiki/home.html')


def article_view(request):
    with open('Django Notes.md', 'rU') as f:
        text_string = f.read()
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        html = md.convert(text_string)

        return render(request, 'wiki/article.html', {'text': html, 'toc': md.toc})