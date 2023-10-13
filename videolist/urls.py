
from .views import *
from django.urls import path

urlpatterns = [
     path('backend/videolist/', video, name="videolist"),
     path('backend/videolist/delete_item/<int:myid>/', delete_item, name="videolist/delete_item"),
     path('backend/videolist/view_item/<int:myid>/', view_item, name="videolist/view_item"),
     path('backend/videolist/activate_catagory/<int:catagory_id>/', activate_catagory, name='videolist/activate_catagory'),
     path('backend/videolist/deactivate_catagory/<int:catagory_id>/', deactivate_catagory, name='videolist/deactivate_catagory'),
 ]


