from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home' ),
    path('signup', views.signup, name='signup'),
    path('logout', views.logUserOut, name='logout'),
    path('login', views.logUserIn, name='login'),
    path('account_verification/<str:pk>', views.accountActivation, name='account_verification'),
    path('forgot_password', views.forgotPassword, name='forgot_password'),
    path('reset_password/<str:pk>', views.resetPassword, name='reset_password'),
    path('reset_password_code/<str:pk>', views.resetPasswordCode, name='password_reset_code'),
    path('update_profile', views.updateProfile, name='update_profile'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow/<str:pk>', views.follow, name='follow'),
    path('unfollow/<str:pk>', views.unfollow, name='unfollow'),

]