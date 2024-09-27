from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from authenticate.models import Follower
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q





# Create your views here.

def home(request):
    pass

@login_required(login_url='home')
def addPost(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text',None)
        video = request.FILES.get('video', None)
        images = request.FILES.getlist('images', None)
        post = Post(user = user, text = text, video = video )
        post.save()
        
        for image in images:
            name = f'{user.username} posted "{text[0:20]}" '
            postImage = Image(image = image, name = name)
            postImage.save()
            post.images.add(postImage)
        if post.text == None and post.video == None and post.images == None:
            post.delete()
            error(request,'cannot post an empty post' )
            return redirect('add_post')
        post.save()
        return redirect('home')
    return render(request, 'posts/addPost.html')


@login_required(login_url='home')
def posts(request):
    following = Follower.objects.filter(follower = request.user)
    posts = Post.objects.filter(user = request.user)
    user = request.user
    if user.is_staff:
        posts = Post.objects.all()
    else:
        for user in following:
            userPosts = Post.objects.filter(user = user.user)
            posts = list(posts) + list(userPosts) 
        posts = list(posts)
        posts.sort(key=lambda x: x.created, reverse=True)
    likes = []
    try:
        likes = Like.objects.filter(user = request.user)
    except:
        pass
    likedPosts = [like.post for like in likes]
    page = 'home'
    posts = posts[:100]
    
    context = {'posts':posts, 'likes': likedPosts, 'page':page}
    return render(request,'posts/posts.html', context)

@login_required(login_url='login')
def trending(request):
    now = timezone.now()
    month = now - timedelta(days = 30)
    posts = list(Post.objects.filter(created__gte = month))
    posts.sort(key=lambda x: x.like + x.comment, reverse=True )
    likes = []
    try:
        likes = Like.objects.filter(user = request.user)
    except:
        pass
    likedPosts = [like.post for like in likes]
    page = 'trending'
    posts = posts[:100]

    context = {'posts':posts, 'likes': likedPosts, 'page':page}
    return render(request,'posts/posts.html', context)
    
@login_required(login_url='login')
def search(request, q):
    q = request.GET.get('q',q)
    posts = []
    if q is not None and q is not ' ':
        posts = Post.objects.filter(text__contains = q.strip()) 
    page = 'search'
    if q is None:
        q = ' '
    context = {'q':q, 'posts':posts, 'page':page, 'section':'posts'}
    return render(request, 'posts/search.html', context)


@login_required(login_url='login')
def searchPeople(request, q):
    user = request.user
    q = request.GET.get('q', q)
    p = q.strip()

    users = User.objects.filter(Q(username__contains = p) |
                                Q(first_name__contains = p) |
                                Q(last_name__contains = p))
    if p is '':
        users = []
    followers = Follower.objects.filter(user = user)
    followers = [follower.follower for follower in followers]
    followings = Follower.objects.filter(follower = user)
    followings = [following.user for following in followings]
    page = 'search'
    context = {'q':q, 'users':users, 'page':page, 'followings':followings, 'followers':followers}
    return render(request, 'posts/search.html', context)





@login_required(login_url='login')
def post(request,pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post__id = post.id)
    likes = Like.objects.filter(post__id = post.id)
    likes = [like.post for like in likes]
    liked = False
    for like in likes:
        if like.user == request.user:
            liked = True
            break

    if request.method == 'POST':
        text = request.POST['comment']
        comment = Comment(user = request.user, text=text, post = post)
        comment.save()
        post.comment += 1
        post.save()
    context = {'post':post, 'comments':comments, 'likes':likes, 'liked':liked}
    return render(request, 'posts/post.html', context)

@login_required(login_url='home')
def like(request, pk):
    post = Post.objects.get(id=pk)
    post.like += 1
    post.save()
    liked = Like(user = request.user, post = post)
    liked.save()
    return redirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(request.path)

@login_required(login_url='home')
def unlike(request,pk):
    post = Post.objects.get(id = pk)
    like = Like.objects.get(post__id = pk , user = request.user)
    post.like -= 1
    post.save()
    like.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='home')
def deletePost(request, pk):
    if request.method == 'POST':

        post = Post.objects.get(id=pk)
        post.delete()
        return redirect('posts')
    return render(request, 'posts/delete.html')

@login_required(login_url='home')
def deleteComment(request, pk):
    if request.method == 'POST':

        comment = Comment.objects.get(id=pk)
        post = comment.post
        post.comment -= 1
        post.save()
        comment.delete()
        return redirect('post', pk=post.id)
    return render(request, 'posts/delete.html')

@login_required(login_url='login')
def editPost(request,pk):
    post = Post.objects.get(id = pk)
    if request.method == 'POST':
        post.text = request.POST.get('text')
        if request.FILES.get('video') is not None:
            post.video = request.FILES.get('video')
        images = request.FILES.getlist('images')
        post.save()
        for image in images:
            name = f'{request.user.username} edited "{post.text[0:20]}" '
            postImage = Image(image = image, name = name)
            postImage.save()
            post.images.add(postImage)
        if post.text != None or post.video != None:
            post.save()
        else:
            error(request, 'Cannot post empty post')
        return redirect('home')
    
    context = {'post':post, 'page':'edit'}
    return render(request, 'posts/addPost.html', context)

@login_required(login_url='login')
def viewComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        reply = Reply(user = request.user, comment = comment, text = text)
        reply.save()
        comment.replies += 1
        comment.save()
    
    replies = Reply.objects.filter(comment = comment)
    context = {'comment': comment, 'replies':replies}
    return render(request, 'posts/comment.html', context)

@login_required(login_url='login')
def deleteReply(request, pk):
    if request.method == 'POST':
        reply = Reply.objects.get(id = pk)
        reply.comment.replies -= 1
        reply.comment.save()
        reply.delete()
        return redirect('comment', pk = reply.comment.id)
    return render(request, 'posts/delete.html')
    
            
