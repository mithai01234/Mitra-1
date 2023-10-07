from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReportViewSet, report, delete_item, activate_catagory, deactivate_catagory, view_item

router = DefaultRouter()
router.register(r'report', ReportViewSet)

urlpatterns = [
    # ... other URL patterns ...
    path('api/', include(router.urls)),
    path('backend/reportlistlist/view_item/<int:myid>/', view_item, name="reportlist/view_item"),

    path('backend/reportlist/',report, name="reportlist"),
    path('backend/reportlist/delete_item/<int:myid>/', delete_item, name="reportlist/delete_item"),
    path('backend/reportlist/activate_catagory/<int:catagory_id>/', activate_catagory, name='reportlist/activate_catagory'),
    path('backend/reportlist/deactivate_catagory/<int:catagory_id>/', deactivate_catagory, name='reportlist/deactivate_catagory'),
] 
