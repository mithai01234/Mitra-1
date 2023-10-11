from .serializers import VideoSerializer, LikeSerializer, CommentUpdateSerializer,CommentSerializer,VideoUpdateSerializer
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Video, Like, Comment
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.conf import settings
from moviepy.editor import VideoFileClip
import os
from registration.models import CustomUser
import moviepy.editor as mp
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from azure.storage.blob import BlobServiceClient, ContentSettings
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings
from django.conf import settings
import uuid
from moviepy.editor import VideoFileClip
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Video
from .serializers import VideoSerializer
from azure.storage.blob import BlobServiceClient, ContentSettings
import moviepy.editor as mp
from PIL import Image
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)

        if serializer.is_valid():
            video_file = request.data.get('file')
            title = serializer.validated_data.get('title', '')

            if not video_file:
                return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Save the uploaded video to a temporary location
                temporary_video_path = self.save_uploaded_video(video_file)

                if not temporary_video_path:
                    return Response({'error': 'Failed to save video'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Compress the video
                compressed_video_path = self.compress_video(temporary_video_path)

                if not compressed_video_path:
                    return Response({'error': 'Failed to compress video'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Initialize the BlobServiceClient
                blob_service_client = BlobServiceClient(
                    account_url=f'https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net',
                    credential=settings.AZURE_ACCOUNT_KEY
                )

                # Get the container client
                container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER)

                # Generate a unique blob name for the video file
                video_blob_name = f'{title}_{uuid.uuid4()}_compressed.mp4'

                # Get the BlobClient for the video file
                video_blob_client = container_client.get_blob_client(video_blob_name)

                # Upload the compressed video to Azure Blob Storage
                with open(compressed_video_path, "rb") as video_data:
                    video_blob_client.upload_blob(video_data, content_settings=ContentSettings(content_type="video/mp4"))

                # Generate a thumbnail from the video and save it
                thumbnail_path = self.generate_and_save_thumbnail(temporary_video_path)

                # Generate a unique blob name for the thumbnail file
                thumbnail_blob_name = f'{title}_{uuid.uuid4()}_thumbnail.jpg'

                # Get the BlobClient for the thumbnail file
                thumbnail_blob_client = container_client.get_blob_client(thumbnail_blob_name)

                # Upload the thumbnail image to Azure Blob Storage
                with open(thumbnail_path, "rb") as thumbnail_data:
                    thumbnail_blob_client.upload_blob(thumbnail_data, content_settings=ContentSettings(content_type="image/jpeg"))

                # Save the video data to the database, including the video and thumbnail blob names
                serializer.save(file=video_blob_name, thumbnail=thumbnail_blob_name)

                # Clean up temporary files
                os.remove(temporary_video_path)
                os.remove(compressed_video_path)
                os.remove(thumbnail_path)

                return Response({'message': 'Video uploaded and compressed successfully'},
                                status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_and_save_thumbnail(self, video_path):
        try:
            # Load the video using MoviePy
            video = mp.VideoFileClip(video_path)

            # Generate the thumbnail from the first frame of the video
            thumbnail = video.get_frame(0)

            # Define the output file path for the thumbnail
            thumbnail_path = "thumbnail.jpg"

            # Save the thumbnail image using PIL
            thumbnail_image = Image.fromarray(thumbnail)
            thumbnail_image.save(thumbnail_path)

            return thumbnail_path
        except Exception as e:
            # Handle any errors that may occur during thumbnail creation
            print(f"Thumbnail creation error: {str(e)}")
            return None


    def save_uploaded_video(self, uploaded_video):
        try:
            # Create a FileSystemStorage instance for saving the uploaded video
            fs = FileSystemStorage()

            # Generate a unique temporary file name
            temporary_video_name = fs.get_available_name("temp_video.mp4")

            # Save the uploaded video to the temporary location
            temporary_video_path = fs.save(temporary_video_name, uploaded_video)

            # Get the full file path of the saved temporary video
            return os.path.join(settings.MEDIA_ROOT, temporary_video_path)
        except Exception as e:
            # Handle any errors that may occur during video saving
            print(f"Video saving error: {str(e)}")
            return None

    def compress_video(self, video_path):
        try:
            # Load the video using MoviePy
            video = mp.VideoFileClip(video_path)

            # Define the output file path for the compressed video
            compressed_video_path = "compressed_video.mp4"

            # Define the target resolution and bitrate (adjust as needed)
            # target_resolution = (640, 360)
            original_width, original_height = video.size

            target_bitrate = "500k"

            # Resize the video to the target resolution
            resized_video = video.resize((original_width, original_height))

            # Write the compressed video to the output file with the specified bitrate
            resized_video.write_videofile(compressed_video_path, codec="libx264", bitrate=target_bitrate)

            return compressed_video_path
        except Exception as e:
            # Handle any errors that may occur during video compression
            print(f"Video compression error: {str(e)}")
            return None


    # def create(self, request, *args, **kwargs):
    #     video_file = request.data.get('file')
    #     user_id = request.data.get('user_id')
    #
    #     if not video_file:
    #         return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         # Load the input video
    #         video = VideoFileClip(video_file.temporary_file_path())
    #
    #         # Define the output video file path in the media/videos directory
    #         output_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'compressed_video.mp4')
    #
    #         # Compress the video and save it to the output file with the desired bitrate
    #         video.write_videofile(output_file_path, codec='libx264', bitrate='500k')
    #
    #         # Close the video object
    #         video.close()
    #
    #         # Retrieve the user object based on the user_id
    #         user = CustomUser.objects.get(id=user_id)
    #
    #         # Create a new Video record in the database with the compressed video file
    #         video = Video(
    #             user_id=user,  # Use the retrieved user object
    #             title=request.data.get('title', ''),  # Extract title from request data
    #             description=request.data.get('description', ''),  # Extract description from request data
    #             file=os.path.relpath(output_file_path, settings.MEDIA_ROOT),  # Save the path relative to MEDIA_ROOT
    #             status=True  # Set the status as needed
    #         )
    #         video.save()
    #
    #         # Return a response indicating success
    #         return Response({'message': 'Video uploaded and compressed successfully'}, status=status.HTTP_201_CREATED)
    #
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get_queryset(self):
        # Get the user ID from the URL parameter (e.g., /api/videos/?user_id=123)
        user_id = self.request.query_params.get('user_id')#only these line will get the params
        hello = Video.objects.all()
        hello = hello.order_by('-uploaded_at')
        # Filter videos by the user ID if it's provided in the query parameter
        if user_id is not None:
            queryset = Video.objects.filter(user_id=user_id)

            # Sort the queryset by the last uploaded date in descending order (newest first)
            queryset = queryset.order_by('-uploaded_at')

            return queryset
        else:
            # If user_id is not provided, return all videos
            return hello

            @action(detail=True, methods=['post'])
            def like(self, request, pk=None):
                video = self.get_object()
                user = request.user
                # Check if the user has already liked the video
                existing_like = Like.objects.filter(user=user, video=video).first()
                if existing_like:
                    # Unlike the video if the user has already liked it
                    existing_like.delete()
                    return Response({"message": "Video unliked successfully"}, status=status.HTTP_200_OK)
                else:
                    # Like the video
                    Like.objects.create(user=user, video=video)
                    return Response({"message": "Video liked successfully"}, status=status.HTTP_201_CREATED)
    # def get_queryset(self):
    #      # Get the user ID from the URL parameter (e.g., /api/videos/?user_id=123)
    #      user_id = self.request.query_params.get('user_id')
    #      # Initialize the BlobServiceClient
    #      blob_service_client = BlobServiceClient(
    #          account_url=f'https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net',
    #          credential=settings.AZURE_ACCOUNT_KEY
    #      )
    #      # Get the container client
    #      container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER)
    #      # List blobs in the container
    #      blob_list = container_client.list_blobs()
    #      # Create a queryset of Video objects based on the user_id
    #      queryset = Video.objects.none()  # Initialize an empty queryset
    #      for blob in blob_list:
    #          # Assuming you have stored the user_id as metadata with the blob
    #          if blob.metadata.get('user_id') == user_id:
    #              video = Video(file=blob.name, title=blob.metadata.get('title', ''),
    #                            description=blob.metadata.get('description', ''))
    #              queryset |= Video.objects.filter(file=blob.name)
    #      # Sort the queryset by the last uploaded date in descending order (newest first)
    #      queryset = queryset.order_by('-uploaded_at')
    #      return queryset

         # @action(detail=True, methods=['post'])
         # def like(self, request, pk=None):
         #     video = self.get_object()
         #     user = request.user
         #     # Check if the user has already liked the video
         #     existing_like = Like.objects.filter(user=user, video=video).first()
         #     if existing_like:
         #         # Unlike the video if the user has already liked it
         #         existing_like.delete()
         #         return Response({"message": "Video unliked successfully"}, status=status.HTTP_200_OK)
         #     else:
         #         # Like the video
         #         Like.objects.create(user=user, video=video)
         #         return Response({"message": "Video liked successfully"}, status=status.HTTP_201_CREATED)
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['post'])  # Set detail to False
    def toggle_like(self, request):
        user_id = request.data.get('user_id')
        video_id = request.data.get('video_id')

        user = get_object_or_404(get_user_model(), pk=user_id)
        video = get_object_or_404(Video, pk=video_id)

        existing_like = Like.objects.filter(user=user, video=video).first()

        if existing_like:
            existing_like.delete()
            message = "Video unliked."
        else:
            Like.objects.create(user=user, video=video, is_like=True)
            message = "Video liked."

        return Response({"message": message}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def like_count(self, request, video_pk=None):
        video_id = request.query_params.get('video_id')

        video = get_object_or_404(Video, pk=video_id)

        likes = Like.objects.filter(video=video, is_like=True)
        like_data = [{'username': like.user.name} for like in likes]

        return Response({"like_count": len(like_data), "likes": like_data}, status=status.HTTP_200_OK)
# Create your views here.


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')

        parent_comment_id = self.request.data.get('parent_comment')
        video_id = self.request.data.get('video')
        serializer.save(
            user_id=user_id,
            video_id=video_id,
            parent_comment_id=parent_comment_id,
        )


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        video_id = self.kwargs['video_id']
        parent_comment_id = self.kwargs.get('parent_comment_id')
        queryset = Comment.objects.filter(video__id=video_id, parent_comment=parent_comment_id).order_by('timestamp')
        return queryset
class ReplyCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        parent_comment_id = self.kwargs['parent_comment_id']
        queryset = Comment.objects.filter(parent_comment=parent_comment_id).order_by('timestamp')
        return queryset


class CommentCountView(generics.RetrieveAPIView):
    def retrieve(self, request, video_id=None):
        def get_comment_data(comment):
            # Get the comment data
            comment_data = {
                'username': comment.user.name,
                'text': comment.text,
            }

            # Get the replies to this comment
            replies = Comment.objects.filter(parent_comment=comment)
            reply_data = []

            for reply in replies:
                # Recursively get data for each reply
                reply_data.append(get_comment_data(reply))

            if reply_data:
                comment_data['replies'] = reply_data

            return comment_data

        # Count top-level comments (comments without parents) for the video
        top_level_comments = Comment.objects.filter(video__id=video_id, parent_comment__isnull=True)
        comment_count = top_level_comments.count()

        # Count replies for the video
        reply_count = Comment.objects.filter(video__id=video_id, parent_comment__isnull=False).count()

        # Calculate the total comment count as the sum of top-level comments and replies
        total_comment_count = comment_count + reply_count

        # Get comments and their associated replies
        comment_data = []

        for comment in top_level_comments:
            comment_data.append(get_comment_data(comment))

        response_data = {
            'video_id': video_id,
            'comment_count': total_comment_count,  # Use the calculated total comment count
            'comments': comment_data,

        }

        return Response(response_data)


class CommentEditView(generics.RetrieveUpdateAPIView):  # Use RetrieveUpdateAPIView to handle both retrieval and update
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer  # Use the serializer for your Comment model

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer






class VideoShareView(generics.UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoUpdateSerializer

    def update(self, request, *args, **kwargs):
        video_id = request.data.get('video_id')
        user_id = request.data.get('user_id')

        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

        video.share_count += 1
        # Optionally, you can associate this action with the user.
        # Assuming you have a 'shared_by' field in your model.
        # video.shared_by.add(user_id)  # Modify this based on your model structure.

        video.save()
        response_data = {
            'share_count': video.share_count
        }
        return Response({'message': 'Video share count incremented successfully.',**response_data}, status=status.HTTP_200_OK)
# class GetVideoLink(APIView):
#     def get(self, request):
#         video_title = request.query_params.get('title')
#
#         if not video_title:
#             return Response({'error': 'Title parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             video = Video.objects.get(title=video_title)
#             video_link = request.build_absolute_uri(settings.MEDIA_URL + video.file.url)
#             return Response({'video_link': video_link}, status=status.HTTP_200_OK)
#         except Video.DoesNotExist:
#             return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
class GetVideoLink(APIView):
    def get(self, request):
        video_title = request.query_params.get('id')

        if not video_title:
            return Response({'error': 'Id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(pk=video_title)
            video_link = request.build_absolute_uri(settings.MEDIA_URL + video.file.name)
            return Response({'video_link': video_link}, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
