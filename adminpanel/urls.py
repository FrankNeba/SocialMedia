from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name = '' ),
    path('signup', views.signup, name='admin_signup'),
    # path('logout', views.logUserOut, name='logout'),
    path('', views.logUserIn, name='admin_login'),
    path('account_verification/<str:pk>', views.accountActivation, name='admin_account_verification'),
    path('forgot_password', views.forgotPassword, name='admin_forgot_password'),
    path('reset_password/<str:pk>', views.resetPassword, name='admin_reset_password'),
    path('reset_password_code/<str:pk>', views.resetPasswordCode, name='admin_password_reset_code'),
    path('update_profile', views.updateProfile, name='admin_update_profile'),
    path('profile/<str:pk>', views.profile, name='admin_profile'),
    path('database', views.database, name='database'),
    path('users', views.siteUsers, name='users'),
    path('posts', views.sitePosts, name='adminposts'),
    path('comments', views.siteComments, name='admincomments'),
    path('replies', views.siteReplies, name='adminreplies'),
    # path('follow/<str:pk>', views.follow, name='follow'),
    # path('unfollow/<str:pk>', views.unfollow, name='unfollow'),

]