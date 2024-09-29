from django.contrib import admin
from core.user.models import User
from core.post.models import Post
from core.comment.models import Comment


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)