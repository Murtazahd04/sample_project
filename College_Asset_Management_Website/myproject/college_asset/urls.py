from django.urls import path
from . import views

app_name = 'college_asset'

urlpatterns = [
    path('register_asset/', views.register_asset, name='register_asset'),
    path('add_classroom/', views.add_classroom, name='add_classroom'),
    path('assign_asset/', views.assign_asset, name='assign_asset'),
    path('classroom_list/', views.classroom_list, name='classroom_list'),
    path('edit_asset/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('edit_classroom/<int:classroom_id>/', views.edit_classroom, name='edit_classroom'),
    path('edit_classroom_asset/<int:classroom_asset_id>/', views.edit_classroom_asset, name='edit_classroom_asset'),
    path('delete_asset/<int:asset_id>/', views.delete_asset, name='delete_asset'),
    path('delete_classroom/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('delete_classroom_asset/<int:classroom_asset_id>/', views.delete_classroom_asset, name='delete_classroom_asset'),
    path('classroom_report/', views.classroom_report, name='classroom_report'),
    path('asset_pie_chart/', views.asset_pie_chart, name='asset_pie_chart'),
]