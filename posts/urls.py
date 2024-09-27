from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='view'),
    path('add_post', views.addPost, name='add_post'),
    path('posts', views.posts, name='posts'),
    path('post/<str:pk>', views.post, name='post'),
    path('like/<str:pk>', views.like, name='like'),
    path('unlike/<str:pk>', views.unlike, name='unlike'),
    path('delete_post/<str:pk>', views.deletePost, name='delete_post'),
    path('delete_comment/<str:pk>', views.deleteComment, name='delete_comment'),
    path('edit_post/<str:pk>', views.editPost, name='edit_post'),
    path('post/comment/<str:pk>', views.viewComment, name='comment'),
    path('delete_reply/<str:pk>', views.deleteReply, name='delete_reply'),
    path('trending', views.trending, name='trending'),
    path('search_posts/<str:q>', views.search, name='search_posts'),
    path('search_people/<str:q>', views.searchPeople, name='search_people'),
]
