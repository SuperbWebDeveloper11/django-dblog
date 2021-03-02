from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def latest_posts(count=5):
    latest_posts = Post.objects.order_by('-created')[:count]
    return {'latest_posts': latest_posts}

