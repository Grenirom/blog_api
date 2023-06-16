from django.db import models

from posts.models import Posts


class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.post}'
