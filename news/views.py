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
        
        for i in scraped_relatedwords:
            if i[0].isdigit():
                i = i.split(".", 1)[-1].strip()  # Remove numbering and strip whitespace
            rwords = i.split(",") 
        
        
        scraped_tt= Trending_topics_news(keyword).split("\n")
        print(type(scraped_tt))
        print(scraped_tt)
        for j in scraped_tt:
            if j[0].isdigit():
                j = j.split(".", 1)[-1].strip()  # Remove numbering and strip whitespace
            tt = j.split(",") 
        # tt=[i.strip() for i in tt]
        # rwords=[i.strip() for i in rwords]
        rwords = [item.strip() for item in rwords if item.strip() != '']    
        tt = [item.strip() for item in tt if item.strip() != '']    


        if scraped_relatedwords is None :
            return Response("Failed to scrape data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data={"Related Words":rwords," Trending Topic":tt}        
        return Response(data)
    

#scraped_authorsnews= authors_news(keyword).split("\n")