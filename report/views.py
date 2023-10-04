from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
def report(request):
    catagoryapp=Report.objects.all()


    context={
        'banform': catagoryapp,


    }
    return render(request,'backend/reportlist.html',context)

def activate_catagory(request, catagory_id):
    banner = get_object_or_404(Report, id=catagory_id)
    banner.status = True
    banner.save()
    return redirect('reportlist')  # Redirect to your banner list view

def deactivate_catagory(request, catagory_id):
    banner = get_object_or_404(Report, id=catagory_id)
    banner.status = False
    banner.save()
    return redirect('reportlist')  # Redirect to your banner list view
# Create your views here.


def delete_item(request, myid):
    report=Report.objects.get(id=myid)
    report.delete()
    return redirect('reportlist')
def view_item(request, myid):
    sel_regform = Report.objects.get(id=myid)

    context = {

        'sel_regform': sel_regform,


    }
    return render(request, 'backend/reportview.html', context)
