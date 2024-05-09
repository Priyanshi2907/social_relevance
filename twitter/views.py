from django.shortcuts import render
from .scraper import *
from .influ_scraper import *
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
        #print("data in view : ",data)      
        return Response(data)
        # return Response(scraped_influencers)

class Influencers(APIView):
    def  get(self, request, keyword):
        #scraped_influencers=(influencers_twitter(keyword))
        scraped_hashtags=(Hashtags_twitter(keyword)).split(' ')
        for i in scraped_hashtags:
             hash=i.split(",")

        scraped_tt=(Trending_topics_twitter(keyword)).split('\n')
        for j in scraped_tt:
             tt=j.split(",")

        hash = [item.strip() for item in hash if item.strip() != '']  
        tt = [item.strip() for item in tt if item.strip() != '']  

        if scraped_hashtags is None :
                return Response("Failed to scrape Data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data={"Top Hashtags":hash,"Trending Topics ":tt}        
        return Response(data)
 

    
    