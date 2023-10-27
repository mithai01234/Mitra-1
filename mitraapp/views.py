from django.shortcuts import render

from relationship.models import Follow
from videoupload.models import Point, Video, Like


def dashboard(request):

    return render(request,'backend/dashboard.html')
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from registration.models import CustomUser, TableJoining  # Adjust your import paths as needed

def user_profile(request, myid):
    user = get_object_or_404(CustomUser, id=myid)
    referred_users = TableJoining.objects.filter(uid=user)
    referred_users_data = []

    for referred_user in referred_users:
        referred_users_data.append({
            'username': referred_user.sponser_id.name,
            'date': referred_user.created_date,
            'income': referred_user.amount,
            'level': referred_user.sponser_id.level,
        })

    user_profile_data = {
        'username_code': user.username_code,
        'level': user.level,
        'total_income': user.total_amount,
        'referred_users': referred_users_data,
    }

    # Render the 'JoiningIncome.html' template with the user profile data
    return render(request, 'backend/JoiningIncome.html', {'user_profile_data': user_profile_data})


def share_income(request, myid):
    user = get_object_or_404(CustomUser, id=myid)

    # Get user's total video shares, likes count, follower count, and following count
    share_count = Video.objects.filter(user_id=user).count()
    like_count = Like.objects.filter(user=user, is_like=True).count()
    follower_count = Follow.objects.filter(followed=user, approved=True).count()
    following_count = Follow.objects.filter(follower=user, approved=True).count()

    # Retrieve the user's points from the Point model
    user_points = None  # Set a default value

    try:
        user_points = Point.objects.get(user=user)
    except Point.DoesNotExist:
        pass  # Optionally, you can handle the case when no Point object is found

    user_profile_data = {
        'username_code': user.username_code,
        'name': user.name,
        'level': user.level,
        'share_count': share_count,
        'like_count': like_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'user_points': user_points.points if user_points else None,  # Include the user's points from the Point model
    }
    # Render the template with the user profile data
    return render(request, 'backend/shareincome.html', {'user_profile_data': user_profile_data})