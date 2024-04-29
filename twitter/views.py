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
        

        if scraped_tweets is None :
            return Response("Failed to scrape Data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data={"tweets":scraped_tweets}  
        print("data in view : ",data)      
        return Response(data)
        # return Response(scraped_influencers)

class Influencers(APIView):
    def  get(self, request, keyword):
        scraped_influencers=(influencers_twitter(keyword))
        scraped_hashtags=(Hashtags_twitter(keyword)).split(' ')
        scraped_tt=(Trending_topics_twitter(keyword)).split('\n')

        if scraped_influencers is None :
                return Response("Failed to scrape Data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data={"Influencers":scraped_influencers,"Top Hashtags":scraped_hashtags,"Trending Topics ":scraped_tt}        
        return Response(data)
 

    
    