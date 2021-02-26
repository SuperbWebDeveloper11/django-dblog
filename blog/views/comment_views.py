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
# import models
from django.contrib.auth.models import User
from ..models import Post, Comment
from ..forms import CommentForm

"""
    # mixins
    RenderListTempMixin: # render list_temp on get request
    RenderDetailTempMixin: # render detail_temp on get request
    RenderCreateTempMixin: # render create_temp on get request
    RenderUpdateTempMixin: # render update_temp on get request
    RenderDeleteTempMixin: # render delete_temp on get request

    # class-based views
    CommentDetail: # render detail_temp on get request 
    CommentCreate: # render create_temp on get request , create new instance on post request
    CommentUpdate: # render update_temp on get request , update instance on post request
    CommentDelete: # render delete_temp on get request , delete instance on post request

"""


# mixin to render list_temp on get request
class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        comment_list = Comment.objects.filter(post=post)
        context = {'comment_list': comment_list, 'post': post }
        data['list_temp'] = render_to_string('blog/comment/partial_comment_list.html', context, request=request)
        return JsonResponse(data)
 

# mixin to render create_temp on get request
class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        if self.badform: # when the user submit a bad form we need to return it back with errors
            data['form_is_valid'] = False
            comment_form = self.badform
        comment_form = CommentForm()
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        context = {'form': comment_form, 'post': post}
        data['create_temp'] = render_to_string('blog/comment/partial_comment_create.html', context, request=request)
        return JsonResponse(data)


# mixin to render update_temp on get request
class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        comment_instance = get_object_or_404(Comment, post=post, pk=kwargs['pk'])
        if self.badform: # when the user submit a bad form we need to return it back with errors
            comment_form = self.badform
        comment_form = CommentForm(instance=comment_instance)
        context = {'form': comment_form, 'post': post}
        data['update_temp'] = render_to_string('blog/comment/partial_comment_update.html', context, request=request)
        return JsonResponse(data)


# mixin to render delete_temp on get request
class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        comment_instance = get_object_or_404(Comment, post=post, pk=kwargs['pk'])
        comment_form = CommentForm(instance=comment_instance)
        context = {'form': comment_form, 'post': post}
        data['delete_temp'] = render_to_string('blog/comment/partial_comment_delete.html', context, request=request)
        return JsonResponse(data)


# mixin to render detail_temp on get request
class RenderDetailTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        comment_instance = get_object_or_404(Comment, post=post, pk=kwargs['pk'])
        context = { 'comment': comment_instance }
        data['detail_temp'] = render_to_string('blog/comment/partial_comment_detail.html', context, request=request)
        return JsonResponse(data)


# render partial_comment_list on get request 
class CommentList(RenderListTempMixin, View):
    pass

# render partial_comment_detail on get request 
class CommentDetail(RenderDetailTempMixin, View):
    pass


# render create_temp on get request , create new instance on post request
class CommentCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid(): 
            post = get_object_or_404(Post, pk=kwargs['post_pk'])
            form.instance.post = post
            form.instance.owner = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render update_temp on get request , update instance on post request
class CommentUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        comment_instance = get_object_or_404(Comment, post=post, pk=kwargs['pk'])
        form = CommentForm(request.POST, request.FILES, instance=comment_instance)
        if form.is_valid():
            if not request.user == comment_instance.owner:
                return HttpResponse('You can not edit this comment')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render delete_temp on get request , delete instance on post request
class CommentDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        comment_instance = get_object_or_404(Comment, post=post, pk=kwargs['pk'])
        if not request.user == comment_instance.owner:
            return HttpResponse('You can not delete this comment')
        comment_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)


