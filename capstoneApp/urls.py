from django.urls import path
from capstoneApp.views import textrunning

urlpatterns = [
    path('textrunning/', textrunning.as_view(), name='API server_2'),
]