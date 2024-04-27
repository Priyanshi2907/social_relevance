from django.shortcuts import render
from .scraper import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SearchTweets(APIView):
    def get(self,request,keyword):
        scraped_tweets = twitter_search(keyword)
        scraped_influencers=influencers_twitter(keyword)
        
        if scraped_influencers is None or scraped_influencers is None:
            return Response("Failed to scrape Data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data={"tweets":scraped_tweets,"Influencers/Top Trending Hashtags/Top Trending Topics":scraped_influencers}        
        return Response(data)
        # return Response(scraped_influencers)
    
    