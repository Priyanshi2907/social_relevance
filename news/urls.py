from django.urls import path
from . views import *

urlpatterns = [
    path('news/<str:keyword>/',SearchNews.as_view(),name="news"),
    path('rwords/<str:keyword>/',relatedwords.as_view(),name="news"),
]



