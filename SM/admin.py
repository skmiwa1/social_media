from django.contrib import admin

from SM.models import Post
from user.models import User

# Register your models here.
admin.site.register(Post)
admin.site.register(User)