from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'article/(?P<slug>.+)/$', views.article_view, name='article'),
    url(r'upload/$', views.UploadView.as_view(), name='upload'),
    url(r'$', views.home, name='home'),
]
