from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'article/(?P<slug>.+)/$', views.article_view, name='view'),
    url(r'upload/$', views.UploadView.as_view(), name='upload'),
    url(r'search/$', views.ArticleSearch.as_view(), name='search'),
    url(r'create/$', views.CreateView.as_view(), name='create'),
    url(r'$', views.home, name='home'),
]
