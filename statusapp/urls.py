from django.urls import path
from . import views

urlpatterns = [
    # ... your existing URL patterns ...

    # Status API endpoints
    path('status/upload/', views.upload_status, name='upload_status'),
    path('status/list/', views.list_statuses, name='list_statuses'),
    path('delete-status/', views.delete_status, name='delete-status'),
]
#/delete-status/?user_id=123&status_id=456
