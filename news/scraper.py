import urllib.request,sys,time
from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import json
from selenium import webdriver
import re
from newspaper import Article
from newspaper import Config
import dateparser
from langdetect import detect
from datetime import datetime, timedelta, date
import pandas as pd
from lxml_html_clean import clean_html
import google.generativeai as genai
    
    
driver = webdriver.Chrome()
GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'

def google_news_scraper(keyword):
    ll = []
    for j in range(0,20,10):
        link = f'https://www.google.co.in/search?q={keyword}+news&sca_esv=64568e91d4c772e8&tbm=nws&prmd=nivsmbtz&sxsrf=ACQVn0-qaS0objyOU3CfpFe1WOR3BQfJHw:1712395312013&ei=MBQRZoQ06-6x4w_n_4nQDA&start={j}&sa=N&ved=2ahUKEwiEjKbSoa2FAxVrd2wGHed_Aso4RhDy0wN6BAgDEAQ&biw=1536&bih=695&dpr=1.25'
        ll.append(link)

    data = []
    for link in ll:  
        driver.get(link)
        driver.implicitly_wait(5)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        news = soup.find_all("div",attrs={'class':"SoaBEf"})
        for row in news:
            des = {}
            title = row.find('div',attrs={'class':"n0jPhd ynAwRc MBeuO nDgy9d"}).text
            url = row.find("a",attrs={'class':"WlydOe"}).get('href')
            source = row.find('div',attrs={'class':"MgUUmf NUnG9d"}).text
            date = row.find('div',attrs={'class':"OSrXXb rbYSKb LfVVr"}).text
            images = row.find('img').get('src')

            des['source'] = source
            des['link'] = url
            des['title'] = title
            des['date'] = date
            des['image'] = images
            data.append(des)

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    

    DATE = []  
    for i in data:
        if i['date']:
            date = dateparser.parse(i['date'])
        if date:
            date = date.strftime("%Y-%m-%d")
            DATE.append(date)

        # article_date = dateparser.parse(article['date'])
        # if article_date and article_date.date() == (datetime.now() - timedelta(days=1)).date():
        #     filtered_data_final.append(article)

    filtered_data = []
    for data1, modified_date in zip(data, DATE):
        if modified_date:
            data1['Modified Dates'] = modified_date
            filtered_data.append(data1)

    filtered_data_final = []
    for data2 in filtered_data:
        if data2['Modified Dates']:
            modified_date = dateparser.parse(data2['Modified Dates'], date_formats=['%Y-%m-%d'])
            modified_date = modified_date.strftime('%Y-%m-%d')
            if modified_date >= yesterday:
                filtered_data_final.append(data2)
    list1 = []
    for item in filtered_data_final:
        title = item['title']
        if detect(title) == 'en':  
            list1.append(item)  

    for item in list1:
        item['title'] = headlines(item['link']) 

    # list1 = [x for x in list1 if isinstance(x, dict) and x.get('title') is not None and ('Error' not in x['title']) and ('Captcha' not in x['title']) and
    #          ('Are you a robot?' not in x['title']) and ('Untitled Page' not in x['title']) and 
    #          ('Subscribe' not in x['title']) and ('You are being redirected...' not in x['title']) and 
    #          ('Not Acceptable!' not in x['title']) and ('403 Forbidden' not in x['title']) and 
    #          ('ERROR: The request could not be satisfied' not in x['title']) and ('Just a moment...' not in x['title']) and 
    #          ('403 - Forbidden: Access is denied.' not in x['title']) and ('Not Found' not in x['title']) and 
    #          ('Page Not Found' not in x['title']) and ('StackPath' not in x['title']) and ('Access denied' not in x['title'])
    #          and ('Yahoo' not in x['title']) and ('Stock Market Insights' not in x['title']) and 
    #          ('Attention Required!' not in x['title']) and ('Access Denied' not in x['title'])
    #          and ('403 forbidden' not in x['title']) and ('Too Many Requests' not in x['title'])
    #          and ('403 - Forbidden' not in x['title']) and ('NCSC' not in x['title'])
    #          and ('BC Gov News' not in x['title']) and ('The Verge' not in x['title']) and ('Trackinsight' not in x['title'])
    #          and ('Morning Headlines' not in x['title']) and ('Forbidden' not in x['title'])
    #          and ('forbidden' not in x['title']) and ('Detroit Free Press' not in x['title'])
    #          and ('reuters.com' not in x['title']) and ('403 unauthorized' not in x['title'])
    #          and ('403 not available now' not in x['title']) and ('Not Acceptable' not in x['title']) 
    #          and ('Your access to this site has been limited by the site owner' not in x['title'])
    #          and ('404 - File or directory not found.' not in x['title'])]

    # for item in list1:
    #     if 'Fortune India: Business News, Strategy, Finance and Corporate ...' in item['source']:
    #         item['source'] = 'Fortune India'

    return list1

def headlines(link):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    link.strip()
    page = Article(str(link), config=config)
    try:
        page.download()
        page.parse()
        return page.title
    except:
        return 'Untitled Page'

#Related Words,influencers,HAshtags,Trending Topic
###########
genai.configure(api_key=GOOGLE_API_KEY)

    
generation_config = {
  "candidate_count": 1,
  "max_output_tokens": 256,
  "temperature": 1.0,
  "top_p": 0.7,
}

safety_settings=[
  {
    "category": "HARM_CATEGORY_DANGEROUS",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]


model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
#     generation_config=generation_config,
    safety_settings=safety_settings
)

def relatedwords_news(keyword):
    """
    Fetches Top Related Keywords for the given keyword
    """
    try:
        
        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the Top 10 Related words for the following Keyword: {keyword}
            in the form of list in a single line and without numbering and any symbol
            
            
            """)

        return response.text
        
    except Exception as e:
        print(e)
        return "No response"
    
def authors_news(keyword):
    """
    Fetches Top  Authors for the given keyword
    """
    try:
        
        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the  Top 10 authors for the following Keyword: {keyword}
            ,in the form of list in a single line and without numbering and any symbol
            
            
            """)

        return response.text
        
    except Exception as e:
        print(e)
        return "No response"

def Trending_topics_news(keyword):
    """
    Fetches Top Trending topics  for the given keyword
    """
    try:

        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the Top Trending Topics for the following Keyword: {keyword}                        
             ,in the form of list in a single line and without numbering and any symbol
            """)

        return response.text
        
    except Exception as e:
        print(e)
        return 'No Response'
    
def take_keyword():
    keyword = input("Enter keyword: ")
    country= input("Enter Country : ")
    keyword += '/' + country
        
    print(f'\n Fetching news  for- {keyword} \n')
    news_data = google_news_scraper(keyword)
    
    relatedwords = relatedwords_news(keyword)
    authors = authors_news(keyword)
    Trending_topics = Trending_topics_news(keyword)

    print(f'\n Top 10 Related Words for {keyword}: \n\n', relatedwords)
    print("Top 10 Authors for {keyword}:", authors)
    print("Top trending topics for {keyword}:", Trending_topics)


    df = pd.DataFrame(news_data)
    print(df)

#take_keyword()