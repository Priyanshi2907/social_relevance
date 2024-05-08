from django.shortcuts import render
from .scraper import *
from . scraper_new import *
from .auth_scraper import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SearchNews(APIView):
    def get(self,request,keyword):
        scraped_news = google_news_scraper_new(keyword)
        
        if scraped_news is None :
            return Response("Failed to scrape data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data={"News":scraped_news}        
        return Response(data)
        #return Response(scraped_news)

class relatedwords(APIView):
    def get(self,request,keyword):
        scraped_relatedwords= relatedwords_news(keyword).split("\n")
        scraped_authorsnews= authors_news(keyword).split("\n")
        scraped_tt= Trending_topics_news(keyword).split("\n")

        if scraped_relatedwords is None :
            return Response("Failed to scrape data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data={"Related Words":scraped_relatedwords,"Authors":scraped_authorsnews," Trending Topic":scraped_tt}        
        return Response(data)
    

