from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('about/',views.about),
    path('posts/',include('posts.urls')),
    path('college_asset/',include('college_asset.urls')),
    path('users/', include('users.urls')),
    
    
]
