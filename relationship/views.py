from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from registration.models import CustomUser
from rest_framework.permissions import BasePermission
from rest_framework_api_key.permissions import HasAPIKey
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
# {
# "target_user_id":18,
# "user_id":13
#  }
@api_view(['GET'])
def get_follow_requests(request):
    user_id = request.GET.get('user_id')

    if user_id is None:
        return Response({'error': 'Missing user_id in query parameters'}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': f'User with ID {user_id} does not exist'}, status=400)

    follow_requests = Follow.objects.filter(follower_id=user.id, approved=False)
    serialized_requests = [{'id': req.id, 'requester': req.follower.name} for req in follow_requests]

    return Response({'follow_requests': serialized_requests})
@api_view(['POST'])
def remove_follow_request(request):
    request_id = request.data.get('request_id')
    user_id = request.data.get('user_id')

    if request_id is None:
        return Response({'error': 'Missing request_id in request data'}, status=400)

    try:
        follow_request = Follow.objects.get(id=request_id, follower=user_id , approved=False,  hidden=False)
    except Follow.DoesNotExist:
        return Response({'error': f'Follow request with ID {request_id} does not exist or is not pending'}, status=400)

    follow_request.delete()
    return Response({'message': f'Follow request with ID {request_id} has been removed'}, status=200)
@api_view(['POST'])

def approve_follow_request(request):
    request_id = request.data.get('request_id')
    user_id = request.data.get('user_id')

    follow_request = get_object_or_404(Follow, id=request_id, follower_id=user_id, approved=False)
    follow_request.approved = True
    follow_request.hidden = True
    follow_request.save()
    return JsonResponse({'message': 'Follow request approved'})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def unfollow(request, name):
#     user_to_unfollow = get_object_or_404(CustomUser, id=name)
#
#     try:
#         # Attempt to retrieve the follow relationship and delete it
#         follow_relation = Follow.objects.get(followed_id=request.user.id, follower_id=user_to_unfollow.id)
#         follow_relation.delete()
#         return JsonResponse({'message': f'You have unfollowed user with ID {name}'})
#     except Follow.DoesNotExist:
#         return JsonResponse({'error': 'Follow relationship does not exist'}, status=400)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def followers_count(request, name):
#     user = get_object_or_404(CustomUser, id=name)
#
#     # Count the number of followers
#     followers_count = Follow.objects.filter(followed=user, approved=True).count()
#
#     return JsonResponse({'followers_count': followers_count})
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])#this only line is responsible for authentication
# def following_count(request, name):
#     user = get_object_or_404(CustomUser, id=name)
#
#     # Count the number of following
#     following_count = Follow.objects.filter(follower=user, approved=True).count()
#
#     return JsonResponse({'following_count': following_count})

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
    followers = Follow.objects.filter(followed=user, approved=True).values_list('follower__name', flat=True)

    return Response({'followers_count': len(followers), 'followers': list(followers)})

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
    following = Follow.objects.filter(follower=user, approved=True).values_list('followed__name', flat=True)

    return Response({'following_count': len(following), 'following': list(following)})
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