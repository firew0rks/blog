from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'(?P<id>\d+)$', views.post, name='post_detail'),
	url(r'test$', views.test, name='test'),
	url(r'text$', views.test2, name='test2')
]