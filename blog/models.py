from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='blog_posts', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
                     
    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='blog_comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

