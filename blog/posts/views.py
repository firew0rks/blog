from django.shortcuts import render

from .models import Post


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