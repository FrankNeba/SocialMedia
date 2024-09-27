from django.shortcuts import render, redirect
from .models import User, Follower
from posts.views import Post, Like
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import random

def mail(message, subject, recipient):
    send_mail(
        subject = subject,
        message= message,
        recipient_list= [recipient],
        from_email='',
        fail_silently=False

    )

def home(request):
    if request.user.is_authenticated:
        return redirect('posts')
    return render(request, 'authenticate/index.html')


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
            message = f'Hello {username},\nYour Socia account verification code is {code}'
            subject = f'Account Verifcation'
            try: 
                mail(message=message, subject=subject, recipient=user.email)
                user.save()
                return redirect('account_verification', pk=user.id)
            except:
                messages.error(request, 'Check your internet connection')
        
    return render(request, 'authenticate/signup.html')

# @login_required(login_url='login')
def accountActivation(request, pk):
    if request.method == 'POST':
        code = int(request.POST['code'])
        user = User.objects.get(id = pk)
        if user.code == code:
            user.is_active = True
            user.save()
            messages.success(request, 'Account verified, login to continue')
            return redirect('login')
        messages.error(request, 'Invalid code')
    page = 'Account Activation'
    context = {'page':page}
    return render(request, 'authenticate/accountActivation.html', context)


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
        if user is not None:
            login(request, user)
            return redirect('home')
                
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
            pass
        messages.error(request,'Incorrect email or password')
    
    return render(request,'authenticate/login.html') 

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            code = random.randint(111111, 999999)
            user.code = code
            message = f'Hello {user.username},\nYour Socia account password reset code is {code}'
            subject = f'Reset password'
            try: 
                mail(message=message, subject=subject, recipient=user.email)
                user.save()
                return redirect('password_reset_code', pk=user.id)
            except:
                messages.error(request, 'Check your internet connection')
        except:
            messages.error(request,f'No user with email {email}')
    
    return render(request, 'authenticate/forgotPassword.html')


def resetPasswordCode(request,pk):
    if request.method == 'POST':
        code = int(request.POST['code'])
        user = User.objects.get(id = pk)
        if user.code == code:
            login(request,user)
            return redirect('reset_password', pk=user.id)
        messages.error(request, 'Invalid code')
    page = 'Password Reset Code'
    context = {'page':page}
    return render(request, 'authenticate/accountActivation.html', context)

@login_required(login_url='login')
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
            return redirect('home')
    return render(request, 'authenticate/resetPassword.html') 

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
    return render(request, 'authenticate/updateProfile.html', {'user':user})
@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST':
        image = request.FILES['image']
        user.image = image
        user.save()

    followers = Follower.objects.filter(user = user)
    followings = Follower.objects.filter(follower = user)
    posts = Post.objects.filter(user = user)
    myfollowers = Follower.objects.filter(user = request.user)
    myfollowers = [follower.follower for follower in myfollowers]
    myfollowings = Follower.objects.filter(follower = request.user)
    myfollowings = [following.user for following in myfollowings]

    context = {'user':user,'posts':posts,'followers':followers, 'myfollowings': myfollowings, 'myfollowers':myfollowers, 'followings': followings}
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


        






# Create your views here.
