from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'1/$', views.article_view, name='article'),
    url(r'$', views.home, name='home'),
]