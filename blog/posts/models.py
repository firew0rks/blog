from django.db import models

class PostTag(models.Model):
	tag = models.SlugField(max_length=20)

	def __str__(self):
		return self.tag

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to='upload', blank=True, null=True)
	author = models.CharField(max_length=20)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(PostTag)

	def __str__(self):
		return self.title

	@property
	def sample_text(self):
		if len(self.text) > 50:
			return self.text[0:50] + '...'

		return self.text[0:50]