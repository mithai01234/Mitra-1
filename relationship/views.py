from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from registration.models import CustomUser
from rest_framework.permissions import BasePermission
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser, Follow

@api_view(['POST'])
def toggle_follow(request):
    target_user_id = request.data.get('target_user_id')
    user_id = request.data.get('user_id')

    if target_user_id is None or user_id is None:
        return Response({'error': 'Missing target_user_id or user_id in request data'}, status=400)

    try:
        # Attempt to retrieve the target user by ID
        target_user = CustomUser.objects.get(id=target_user_id)
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'User with ID {target_user_id} or {user_id} does not exist'}, status=400)

    # Check if a follow relationship already exists
    follow_relationship = Follow.objects.filter(followed_id=user.id, follower_id=target_user.id).first()

    if follow_relationship:
        # If a relationship exists, delete it to unfollow the user
        follow_relationship.delete()
        return Response({'message': f'Unfollowed user with ID {target_user_id}'}, status=200)
    else:
        # If no relationship exists, create a new follow request
        Follow.objects.create(followed_id=user.id, follower_id=target_user.id)
        return Response({'message': f'Follow request sent to user with ID {target_user_id}'}, status=201)


@api_view(['GET'])
def get_follow_requests(request):
    user_id = request.GET.get('user_id')

    if user_id is None:
        return Response({'error': 'Missing user_id in query parameters'}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'User with ID {user_id} does not exist'}, status=400)

    follow_requests = Follow.objects.filter(followed_id=user.id, approved=False)

    serialized_requests = [{'id': user.id,'name':user.name,'requester_id': req.follower.id} for req in follow_requests]

    return Response({'follow_requests': serialized_requests})


@api_view(['POST'])
def remove_follow_request(request):
    requester_id = request.data.get('requester_id')
    user_id = request.data.get('user_id')

    if requester_id is None:
        return Response({'error': 'Missing requester_id in request data'}, status=400)

    try:
        requester = CustomUser.objects.get(id=requester_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'Requester with ID {requester_id} does not exist'}, status=400)

    # Find and delete the pending follow request sent by the requester to the user
    follow_request = Follow.objects.filter(follower=requester, followed_id=user_id, approved=False, hidden=False).first()

    if follow_request:
        follow_request.delete()
        return Response({'message': f'Follow request from requester with ID {requester_id} has been removed'}, status=200)
    else:
        return Response({'error': 'No pending follow request from the requester to the user'}, status=400)


# @api_view(['POST'])
# def approve_follow_request(request):
#     request_id = request.data.get('request_id')
#     user_id = request.data.get('user_id')
#
#     try:
#         follow_request = Follow.objects.get(id=request_id, followed_id=user_id, approved=False, hidden=False)
#     except Follow.DoesNotExist:
#         return Response({'error': f'Follow request with ID {request_id} does not exist or is not pending'}, status=400)
#
#     follow_request.approved = True
#     follow_request.hidden = True
#     follow_request.save()
#     return Response({'message': 'Follow request approved'}, status=200)
@api_view(['POST'])
def approve_follow_request(request):
    user_id = request.data.get('user_id')
    requester_id = request.data.get('requester_id')

    try:
        user = CustomUser.objects.get(id=user_id)
        requester = CustomUser.objects.get(id=requester_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'User with ID {user_id} or {requester_id} does not exist'}, status=400)

    # Check if there is a pending follow request from the requester to the user
    follow_request = Follow.objects.filter(follower=requester, followed=user, approved=False, hidden=False).first()

    if follow_request:
        # Approve the follow request
        follow_request.approved = True
        follow_request.hidden = True
        follow_request.save()

        return Response({'message': 'Follow request approved', 'requester_id': requester.id}, status=200)
    else:
        return Response({'error': 'No pending follow request from the requester to the user'}, status=400)

@api_view(['GET'])
def followers_count(request):
    user_id = request.GET.get('user_id')

    if user_id is None:
        return Response({'error': 'Missing user_id in query parameters'}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'User with ID {user_id} does not exist'}, status=400)

    # Retrieve the followers with approved follow relationships
    followers = Follow.objects.filter(followed=user, approved=True)

    # Extract the IDs and names of the followers
    followers_data = [{'id': follower.follower_id, 'name': follower.follower.name} for follower in followers]

    return Response({'followers_count': len(followers_data), 'followers': followers_data})


# Define the 'following_count' view similarly as 'followers_count' for users the specified user is following.


@api_view(['GET'])
def following_count(request):
    user_id = request.GET.get('user_id')

    if user_id is None:
        return Response({'error': 'Missing user_id in query parameters'}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'User with ID {user_id} does not exist'}, status=400)

    # Retrieve the users that the specified user is following with approved follow relationships
    following = Follow.objects.filter(follower=user, approved=True)

    # Extract the IDs and names of the users being followed
    following_data = [{'id': followed.followed_id, 'name': followed.followed.name} for followed in following]

    return Response({'following_count': len(following_data), 'following': following_data})

@api_view(['POST'])
def block_user(request):
    user_id = request.data.get('user_id')
    user_to_block_id = request.data.get('user_to_block_id')

    if user_id is None or user_to_block_id is None:
        return Response({'error': 'Missing user_id or user_to_block_id in request data'}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
        user_to_block = CustomUser.objects.get(id=user_to_block_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'One or both users do not exist'}, status=400)

    if user_id != user_to_block_id:
        user.blocked_users.add(user_to_block)
        return Response({'message': f'You have blocked {user_to_block.name}'})

    return Response({'error': 'You cannot block yourself'})
@api_view(['POST'])
def unblock_user(request):
    user_id = request.data.get('user_id')
    user_to_unblock_id = request.data.get('user_to_unblock_id')

    if user_id is None or user_to_unblock_id is None:
        return Response({'error': 'Missing user_id or user_to_unblock_id in request data'}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
        user_to_unblock = CustomUser.objects.get(id=user_to_unblock_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'One or both users do not exist'}, status=400)

    if user_to_unblock in user.blocked_users.all():
        user.blocked_users.remove(user_to_unblock)
        return Response({'message': f'You have unblocked {user_to_unblock.name}'})

    return Response({'error': f'{user_to_unblock.name} is not in your blocked users list'})