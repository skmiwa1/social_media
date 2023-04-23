from django.contrib import admin

from SM.models import Post, Like
from user.models import User

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Like)
