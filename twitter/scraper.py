# scraper.py

import requests
from datetime import datetime, timedelta
import pandas as pd
import google.generativeai as genai

# Pass your Gemini API key here 

GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'

def twitter_search(keyword):
    '''
    Searches for the Tweets with certain keyword  
    '''
    url = "https://twitter154.p.rapidapi.com/search/search"
    #print(url)
    today = datetime.today()
    yesterday = today - timedelta(days=4000)
    yesterday = yesterday.strftime('%Y-%m-%d')
    
    querystring = {
        "query": keyword,
        "section": "top",
        "min_retweets": "1",
        "min_likes": "1",
        "limit": "20",
        "start_date": yesterday,
        "language": "en"
    }
    
    headers = {
    	"X-RapidAPI-Key":  "ab7352931fmsh344160b283158fap188f76jsn220404eb19f6",  # Rapid API key
    	"X-RapidAPI-Host": "twitter154.p.rapidapi.com" 
    }
    
   
    
   
    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(response.json())
    for tweet in response.json()['results']:
        #print (tweet['text'])
        #if keyword.lower() in tweet['text'].lower() :
            try:   
                
                data_2 = [{
                    "tweet_id": tweet['tweet_id'],
                    "text": tweet['text'].replace("&amp;","&").replace("&gt;",">") ,  
                    "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
                    "tweet_link": tweet['expanded_url'],
                    "user_screen_name": tweet['user']['username'],
                    "user_followers_count": tweet['user'].get('follower_count', 0),
                    "username": tweet['user']['name'],                    
                    "user_profile_link": 'https://twitter.com/' + tweet['user']['username']
                } for tweet in response.json()['results'] if all(tweet.get(key) for key in ['tweet_id', 'text', 'creation_date', 'expanded_url', 'user'])
                and tweet['user'].get('follower_count')>=2000 
                and keyword.split(" ")[0].lower() in tweet['text'].lower()
                and keyword.split(" ")[-1].lower() in tweet['text'].lower()]
        
            except Exception as e:
                data_2 = [{
                    "tweet_id": tweet['tweet_id'],
                    "text": tweet['text'].replace("&amp;","&").replace("&gt;",">") ,  
                    "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
                    "tweet_link": tweet['expanded_url'],
                    "user_screen_name": tweet['user']['username'],
                    "user_followers_count": tweet['user'].get('follower_count', 0),
                    "username": tweet['user']['username'],
                    "user_profile_link": 'https://twitter.com/' + tweet['user']['username']

                } for tweet in response.json()['results'] 
                if all(tweet.get(key) for key in ['tweet_id', 'text', 'creation_date', 'expanded_url', 'user'])
                and tweet['user'].get('follower_count')>=2000 
                and keyword.split(" ")[0].lower in tweet['text'].lower()
                and keyword.split(" ")[-1].lower() in tweet['text'].lower()]

            data_2_sorted = sorted(data_2, key=lambda x: x['user_followers_count'], reverse=True)   
            return data_2_sorted
            # df=pd.DataFrame(data_2)
            # print(df)
            
    
    
      # Return None to indicate failure
# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.

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

# def influencers_twitter(keyword):
#     """
#     Fetches Top Influencers ,Hashtags ,Top trending Topics for the given keyword
#     """
#     try:

#         response = model.generate_content(f"""
  
#              You are a helpful assistant that will help me in finding the Top 10 Influencers with thier name and clickable twitter profile links for the following Keyword: {keyword}
#             in a format for example ["Name of Influencer 1" : "Twitter link" , "Name of Influencer 2" : "Twitter link" and so on], without numbering  and without "\"  and should be in a single line            """)

#         return response.text
        
#     except Exception as e:
#         print(e)
#         return 'No Response'

# def Hashtags_twitter(keyword):
#     """
#     Fetches Top Hashtags  for the given keyword
#     """
#     try:

#         response = model.generate_content(f"""
  
#             You are a helpful assistant that will help me in finding the Top 10 Trending Hashtags  for the following Keyword: {keyword}                        
#             seperated by only space,in the form of list,in a single line
            
#             """)

#         return response.text
        
#     except Exception as e:
#         print(e)
#         return 'No Response'

# def Trending_topics_twitter(keyword):
#     """
#     Fetches Top Trending topics  for the given keyword
#     """
#     try:

#         response = model.generate_content(f"""
  
#             You are a helpful assistant that will help me in finding the Top Trending Topics for the following Keyword: {keyword}                        
#             ,in the form of list, in a single line, only the topics without any symbol and numbering
#             """)

#         return response.text
        
#     except Exception as e:
#         print(e)
#         return 'No Response'

def getresponse():
    keyword=input("Enter keyword for twitter: ")
    country=input("enter country for twitter: ")
    
    keyword += '/' + country
        
    print(f'\n Fetching tweets for- {keyword} \n')

    df_twitter=twitter_search(keyword)
    # top_influencers = (influencers_twitter(keyword))
    # top_hashtags = (Hashtags_twitter(keyword)).split(' ')
    # top_trending_topics = (Trending_topics_twitter(keyword)).split(' ')

    
    # print(f'\n Top 10 Influencers for {keyword}: \n\n', type(top_influencers))    
    # print(f'\n Top 10 Influencers for {keyword}: \n\n', top_influencers)    

    #print("Top 10 Hashtags for {keyword}:", (top_hashtags))
    #print("Top trending topics for {keyword}:", top_trending_topics)


    print(df_twitter)

    return df_twitter

#getresponse()
