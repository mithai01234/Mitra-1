from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import CustomUser
from rest_framework import generics
from registration.serializers import CustomUserSerializer
def registerlist(request):
    registerapp=CustomUser.objects.all()
    context={
        'regform': registerapp



    }
    return render(request,'backend/registerList.html',context)
class CustomUserList(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

def view_item(request, myid):
    sel_regform = CustomUser.objects.get(id=myid)
    reg = CustomUser.objects.all()
    context = {
        'regform': reg,
        'sel_regform': sel_regform

    }
    return render(request, 'backend/registerview.html', context)
def activate_catagory(request, catagory_id):
    banner = get_object_or_404(CustomUser, id=catagory_id)
    banner.status = 1
    banner.save()
    return redirect('userlist')  # Redirect to your banner list view

def deactivate_catagory(request, catagory_id):
    banner = get_object_or_404(CustomUser, id=catagory_id)
    banner.status = 2
    banner.save()
    return redirect('userlist')  # Redirect to your banner list view
# Create your views here.
def suspend_user(request, catagory_id):
    banner = get_object_or_404(CustomUser, id=catagory_id)
    banner.status = 3
    banner.save()


    return redirect('userlist')  # Redirect to your category list view
