from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from .models import Post

# Create your views here.
def home(request):
	'''
	Displays the last 5 posts
	'''
	
	# Getting the last 5 posts
	p = Post.objects.all().order_by('id')[:5]

	# Rendering the last 5 points onto webpage
	return render(request, 'home.html', {'posts': p})

def post(request, id):
	'''
	Displays an the actual post retrieved by the ID of the post
	'''
	return HttpResponse('Hello World!')