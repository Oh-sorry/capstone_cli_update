
from django.contrib import admin
from django.urls import path, include
from capstoneApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('index/', views.index),
    path('login/', views.login),
    path('signup/', views.signup),
    path('textrunning/', views.textrunning),
]