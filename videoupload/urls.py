from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentCreateView,GetVideoLink, CommentListView,VideoShareView, ReplyCommentListView, LikeViewSet, CommentCountView,CommentEditView, CommentDeleteView
from .views import VideoViewSet
router = DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    # ... other URL patterns ...
    path('api/', include(router.urls)),
    path('videos/toggle_like/', LikeViewSet.as_view({'post': 'toggle_like'}), name='video-toggle-like'),
    path('likes/like_count/',LikeViewSet.as_view({'get': 'like_count'}), name='video-like-count'),
    path('comment/', CommentCreateView.as_view(), name='comment-create'),
    # path('comment/<int:pk>/', CommentEditView.as_view(), name='comment-edit-delete'),  # Edit and Delete Comment
    # path('comments/<int:video_id>/', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:parent_comment_id>/replies/', ReplyCommentListView.as_view(), name='reply-comment-list'),
    path('comment-count/<str:video_id>/', CommentCountView.as_view(), name='comment-count'),
    path('comments/<int:pk>/edit/', CommentEditView.as_view(), name='comment-edit'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('api/get_video_link/', GetVideoLink.as_view(), name='get_video_link'),#get the video link
    path('videos/share/', VideoShareView.as_view(), name='video-share'),
]
