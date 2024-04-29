from django.urls import path
from . views import *

urlpatterns = [
    path('tweets/<str:keyword>/',SearchTweets.as_view(),name="tweets"),
    path('influencers/<str:keyword>/',Influencers.as_view(),name="inf"),

]
