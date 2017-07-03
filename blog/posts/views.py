from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Post, NextModel


# Create your views here.
def home(request):
	"""
	Displays the last 5 posts
	"""
	
	# Getting the last 5 posts
	p = Post.objects.all().order_by('id')[:5]

	# Rendering the last 5 points onto webpage
	return render(request, 'home.html', {'posts': p})


def post(request, id):
	"""
	Displays an the actual post retrieved by the ID of the post 
	"""
	try:
		p = Post.objects.get(id=id)
		post_tags = p.tags.all()
	except:
		# In case someone tries a random number
		return render(request, 'page_unknown.html')

	return render(request, 'post.html', {'post': p, 'tags': post_tags})


def test(request):
	u = NextModel()
	u.title = 'this is a title2!'
	u.text = 'kittywowow'
	u.abstract = 'abcdefgg'
	u.save()
	return HttpResponseRedirect(reverse('home'))


def test2(request):
	try:
		u = NextModel.objects.get(text='kitty')
		print(u.title)
		print(u.text)
		print(u.abstract)
	except:
		print('cant find it')

	return HttpResponseRedirect(reverse('home'))