from django.contrib import admin
from .models import Post, PostTag

# Register your models here.
class PostAdmin(admin.ModelAdmin):
	pass

class PostTagAdmin(admin.ModelAdmin):
	pass

admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)