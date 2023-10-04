from django.shortcuts import render
from videoupload.models import Video
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import CustomUser
from azure.storage.blob import BlobServiceClient

def video(request):
    # Assuming you have a Video model with a field named 'video_blob_name'
    videos = Video.objects.all()



    context = {
        'banform': videos,
    }

    return render(request, 'backend/videolist.html', context)

def view_item(request, myid):
    sel_regform = Video.objects.get(id=myid)

    context = {

        'sel_regform': sel_regform,


    }
    return render(request, 'backend/videoview.html', context)

def activate_catagory(request, catagory_id):
    banner = get_object_or_404(Video, id=catagory_id)
    banner.status = True
    banner.save()
    return redirect('videolist')  # Redirect to your banner list view

def deactivate_catagory(request, catagory_id):
    banner = get_object_or_404(Video, id=catagory_id)
    banner.status = False
    banner.save()
    return redirect('videolist')  # Redirect to your banner list view
# Create your views here.
def delete_item(request, myid):
    video=Video.objects.get(id=myid)
    video.delete()
    return redirect('videolist')