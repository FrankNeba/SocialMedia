from django.shortcuts import render, redirect
from authenticate.models import *
from posts.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db.models import Q
import random

def mail(message, subject, recipient):
    send_mail(
        subject = subject,
        message= message,
        recipient_list= [recipient],
        from_email='Socia',
        fail_silently=False

    )

def home(request):
    return render(request, 'adminpanel/index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']
        email = request.POST['email']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f'An account exists with email {email}')
        
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'An account exists with username {username}')

        elif password != passwordConfirm:
            messages.error(request, 'Passwords don\'t match')

        elif len(password) < 8:
            messages.error(request, 'Password too short')

        # elif True:
            # messages.error(request, 'Password can easily be guessed')

        else: 
            code = random.randint(11111, 99999)
            user = User(username=username, email=email, password = make_password(password))
            user.code = code
            user.is_active = False
            user.save()
            login(request, user)
            message = f'Hello {username},\nYour Socia account verification code is {code}'
            subject = f'Account Verifcation'
            mail(message=message, subject=subject, recipient=user.email)
            return redirect('admin_account_verification', pk=user.id)
    auth = 'admin'
    context = {'auth': auth}  
    return render(request, 'authenticate/signup.html' , context)

# @login_required(login_url='login')
def accountActivation(request, pk):
    if request.method == 'POST':
        code = int(request.POST['code'])
        user = User.objects.get(id = pk)
        if user.code == code:
            user.is_active = True
            user.is_staff = True
            user.save()
            messages.success(request, 'Account verified, login to continue')
            return redirect('admin_login')
        messages.error(request, 'Invalid code')
    return render(request, 'adminpanel/accountActivation.html')


@login_required(login_url='login')
def logUserOut(request):
    logout(request)
    return redirect('home')


def logUserIn(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password= password)
        

        #if user exists and authentication is correct
        if user is not None :
            if user.is_staff:
                login(request, user)
                messages.error(request, 'You are loged in as admin')

            else:
                messages.error(request, 'You are not allowed to access this site')
                return redirect(request.META.get('HTTP_REFERER'))
            return redirect('database')

                
        try:
            user = User.objects.get(email = email)
            if user.check_password(password):
                code = random.randint(111111, 999999)
                user.code = code
                user.save()
                message = f'Hello {user.username},\nYour Socia account is not activated.\nYour Socia account verification code is {code}'
                subject = f'Account Verifcation'
                mail(message=message, subject=subject, recipient=user.email)
                messages.success(request,'Account not vierified. ')
                return redirect('account_verification', pk=user.id)
        
        except:
            messages.error(request,'incorrect email or password')
    auth = 'admin'
    context = {'auth': auth}
    
    return render(request,'authenticate/login.html', context) 

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            code = random.randint(111111, 999999)
            user.code = code
            user.save()
            message = f'Hello {user.username},\nYour Socia account password reset code is {code}'
            subject = f'Reset password'
            mail(message=message, subject=subject, recipient=user.email)
            return redirect('password_reset_code', pk=user.id)
        except:
            messages.error(request,f'No user with email {email}')
    
    return render(request, 'adminpanel/forgotPassword.html')

def resetPasswordCode(request,pk):
    if request.method == 'POST':
        code = int(request.POST['code'])
        user = User.objects.get(id = pk)
        if user.code == code:
            return redirect('reset_password', pk=user.id)
        messages.error(request, 'Invalid code')
    return render(request, 'adminpanel/accountActivation.html')

def resetPassword(request, pk):
    if request.method == 'POST':
        password = request.POST['password']
        passwordConfirm = request.POST['passwordConfirm']

     
        if password != passwordConfirm:
            messages.error(request, 'Passwords don\'t match')

        elif len(password) < 8:
            messages.error(request, 'Password too short')

        elif str.isdigit(password):
            messages.error(request,'Password can easily be guessed. Use a combination of numbers, letters and symbols')

        else:
            user = User.objects.get(id = pk)
            user.password = make_password(password)
            user.save()
            return redirect('login')
    return render(request, 'adminpanel/resetPassword.html') 

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['firstname']
        user.last_name= request.POST['lastname']
        if request.FILES.get('image') is not None:
            user.image = request.FILES.get('image')
        user.save()
        messages.success(request,'Profile Updated succesfully')
    return render(request, 'adminpanel/updateProfile.html', {'user':user})
@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id = pk)
    followers = Follower.objects.filter(user = user)
    followings = Follower.objects.filter(follower = user)
    posts = Post.objects.filter(user = user)

    context = {'user':user,'posts':posts,'followers':followers, 'followings': followings}
    return render(request, 'authenticate/profile.html', context)


@login_required(login_url='login')
def follow(request, pk):
    follower = request.user
    user = User.objects.get(id = pk)
    follow = Follower(user = user, follower = follower)
    follow.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def unfollow(request,pk):
    follower = request.user
    user = User.objects.get(id = pk)
    follow = Follower.objects.get(user = user, follower = follower)
    follow.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def database(request):
    if request.user.is_staff:
        page = 'admin'
        context = {'page':page}
        return render(request, 'adminpanel/database.html', context)
    return HttpResponse('You are not allowed to access this page')


@login_required(login_url='login')
def siteUsers(request):
    q = request.GET.get('q','')
    users = User.objects.filter(Q(username__contains = q) | 
                                Q(first_name__contains = q) |
                                Q(last_name__contains = q))
    page = 'admin'
    if request.method == 'POST':
        delete = request.POST.getlist('user')
        for id in delete:
            user = User.objects.get(id = id)
            user.delete()
    
    context = {'users':users, 'page':page}
    return render(request, 'adminpanel/users.html', context)

@login_required(login_url='login')
def sitePosts(request):
    q = request.GET.get('q','')
    posts = Post.objects.filter(Q(text__contains = q)|
                                      Q(user__username__contains = q))
    page = 'admin'
    for post in posts:
        post.text = post.text[:20]
    if request.method == 'POST':
        delete = request.POST.getlist('post')
        for id in delete:
            post = Post.objects.get(id = id)
            post.delete()
        return redirect('adminposts')
    
    context = {'posts':posts, 'page':page,'q':q}
    return render(request, 'adminpanel/posts.html', context)


@login_required(login_url='login')
def siteComments(request):
    q = request.GET.get('q','')
    comments = Comment.objects.filter(Q(text__contains = q)|
                                      Q(user__username__contains = q))
    page = 'admin'
    for comment in comments:
        comment.text = comment.text[:20]
    if request.method == 'POST':
        delete = request.POST.getlist('comment')
        for id in delete:
            comment = Comment.objects.get(id = id)
            comment.delete()
        return redirect('adminposts')
    
    context = {'comments':comments, 'page':page, 'q':q}
    return render(request, 'adminpanel/comments.html', context)


@login_required(login_url='login')
def siteReplies(request):
    q = request.GET.get('q','')
    replies = Reply.objects.filter(Q(text__contains = q)|
                                      Q(user__username__contains = q))
    page = 'admin'
    for reply in replies:
        reply.text = reply.text[:20]
    if request.method == 'POST':
        delete = request.POST.getlist('reply')
        for id in delete:
            reply = Reply.objects.get(id = id)
            reply.delete()
        return redirect('adminposts')
    
    context = {'replies':replies, 'page':page,'q':q}
    return render(request, 'adminpanel/replies.html', context)


# Create your views here.



# Create your views here.
