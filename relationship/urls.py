from django.urls import path
from . import views

urlpatterns = [
    # Send Follow Request
    path('follow/send/', views.toggle_follow, name='send_follow_request'),

    # Get Follow Requests
     path('follow/requests/', views.get_follow_requests, name='get_follow_requests'),
 path('remove/requests/', views.remove_follow_request, name='get_follow_requests'),
    #
    # # Approve Follow Request
     path('follow/approve/', views.approve_follow_request, name='approve_follow_request'),
    #
    # # Unfollow a User
    #  path('unfollow/<str:name>/', views.unfollow, name='unfollow_user'),
    #
    # # Get Followers Count
     path('followers/count/', views.followers_count, name='followers_count'),
    #
    # # Get Following Count
     path('following/count/', views.following_count, name='following_count'),

 path('block/', views.block_user, name='block_user'),

 # Unblock a User
 path('unblock/', views.unblock_user, name='unblock_user'),
]
