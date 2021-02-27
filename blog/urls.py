from django.urls import include, path
from .views import post_views, comment_views

app_name = 'blog'

urlpatterns = [

    ####################### urls for 'posts' curd operations #######################
    path('', post_views.PostList.as_view(), name='post_list'),
    path('tag/<int:tag_pk>/', post_views.PostListByTag.as_view(), name='post_list_by_tag'),
    path('add/', post_views.PostCreate.as_view(), name='post_add'),
    path('<int:pk>/detail/', post_views.PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update/', post_views.PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', post_views.PostDelete.as_view(), name='post_delete'),


    ####################### urls for 'comment' crud operatinons with jQuery #######################
    path('<int:post_pk>/comment/', comment_views.CommentList.as_view(), name='comment_list'),
    path('<int:post_pk>/comment/add/', comment_views.CommentCreate.as_view(), name='comment_create'),
    path('<int:post_pk>/comment/<int:pk>/detail/', comment_views.CommentDetail.as_view(), name='comment_detail'),
    path('<int:post_pk>/comment/<int:pk>/update/', comment_views.CommentUpdate.as_view(), name='comment_update'),
    path('<int:post_pk>/comment/<int:pk>/delete/', comment_views.CommentDelete.as_view(), name='comment_delete'),

]


