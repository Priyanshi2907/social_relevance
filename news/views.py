from django.shortcuts import render
from .scraper import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SearchNews(APIView):
    def get(self,request,keyword):
        scraped_news = google_news_scraper(keyword)
        scraped_influencers= influencers_news(keyword)
        if scraped_influencers is None or scraped_influencers is None:
            return Response("Failed to scrape data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data={"News":scraped_news," Related Words/Authors/Top Trending Topics":scraped_influencers}        
        return Response(data)
        #return Response(scraped_news)
    

