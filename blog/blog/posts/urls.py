from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'(?P<id>\d+)$', views.home, name='post_detail')
]