from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# import Tag model
from taggit.models import Tag
# import models
from django.contrib.auth.models import User
from ..models import Post, Comment


################## views for post crud operations ################## 

class PostList(ListView): # retrieve all posts
    model = Post
    template_name = 'blog/post/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5


class PostListByTag(ListView): # retrieve posts filtred by tags
    model = Post
    template_name = 'blog/post/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['tag_pk'])
        post_list = Post.objects.filter(tags__in=[tag])
        return post_list


class PostDetail(DetailView): # retrieve post detail
    model = Post
    template_name = 'blog/post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = self.get_object()
        context['comment_list'] = Comment.objects.filter(post=current_post)
        return context


class PostCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create new post 
    model = Post
    template_name = 'blog/post/post_form_create.html' 
    fields = ['title', 'body', 'tags']
    success_message = "post was created successfully"

    def form_valid(self, form):
        form.instance.owner = self.request.user # add post owner manually
        return super().form_valid(form)


class PostUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update post 
    model = Post
    template_name = 'blog/post/post_form_update.html' 
    fields = ['title', 'body', 'tags']
    success_message = "post was updated successfully"

    def form_valid(self, form):
        if form.instance.owner == self.request.user: # user should be the post owner 
            return super().form_valid(form)
        else:
            return HttpResponse('You are not post owner')

class PostDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView): # delete post 
    model = Post
    template_name = 'blog/post/post_confirm_delete.html' 
    success_message = "post was deleted successfully"
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if form.instance.publisher == self.request.user: # user should be the post owner 
            return super().form_valid(form)
        else:
            return HttpResponse('you are not post owner')


