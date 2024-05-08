import requests
import pandas as pd
import json
from datetime import datetime,timedelta

def google_news_scraper_new(keyword):
    print("keyword is this ,",keyword)
    url = "https://google-news13.p.rapidapi.com/search"
    
    today = datetime.today().strftime('%Y-%m-%d')
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    

    querystring = {"keyword":keyword,
                   "lr" : 'en-US',
                   
                   }

    headers = {
    "X-RapidAPI-Key": "05a63cbb40mshb60cea8eed8b55bp1b2a8ejsn1037cb90c0d5",
                      #"05a63cbb40mshb60cea8eed8b55bp1b2a8ejsn1037cb90c0d5"
    "X-RapidAPI-Host": "google-news13.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        print(response.json())
        unique_url=set()
        #data=[]
        for idx,news in enumerate(response.json()['items']):
            if idx>=10:
                break
            # if news['newsUrl'] in unique_url:
            #     continue
            # unique_url.add(news['newsUrl'])
            data=[{
                    'source': news['publisher'],
                    'link': news['newsUrl'],
                    'title': news['title'],
                    'image': news['images']['thumbnailProxied'],
                    "Modified Dates": timestamp_to_date(news['timestamp'])

            } for news in response.json()['items'] if timestamp_to_date(news['timestamp']) >= yesterday ]

            #if all(news.get(key) for key in ['publisher', 'newsUrl', 'title', 'images', 'timestamp'])]
    
            return data
            
    except requests.exceptions.RequestException as e:
         print("Error:", e)
         return None
    df=pd.DataFrame(data)
    print("df in function : ",df)

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(int(timestamp) // 1000).strftime("%Y-%m-%d")

def main():
    keyword=input("enter keyword for news : ")
    country=input("enter country for news : ")
    keyword += '/' + country

    print(f'\n Fetching  new news for- {keyword} \n')

    output=google_news_scraper_new(keyword)
    if output:
        df = pd.DataFrame(output)
        print("Output in main:")
        print(df)
    else:
        print("No data fetched from the API.")
#main()


