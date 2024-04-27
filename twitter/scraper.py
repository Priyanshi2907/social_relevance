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
    
    today = datetime.today()
    yesterday = today - timedelta(days=1)
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
    	'X-RapidAPI-Key': 'f7173b49d5msh09de40987862b60p194beajsn834236db5d67',
      'X-RapidAPI-Host': 'twitter154.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data_2 = [{
            "tweet_id": tweet['tweet_id'],
            "text": tweet['text'],
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "tweet_link": tweet['expanded_url'],
            "user_screen_name": tweet['user']['username'],
        } for tweet in response.json()['results']]
        return data_2
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None  # Return None to indicate failure
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

def influencers_twitter(keyword):
    """
    Fetches Top Influencers and Hashtags for the given keyword
    """
    try:

        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the Top 10 Influencers with thier clickable and activate profile links and Top Trending Hashtags for the following Keyword: {keyword}
            And also Top trending topics in the world.
            
            Output should contain only Influencers names and any one of their clickable social handles.
            
            """)

        return response.text
        
    except Exception as e:
        print(e)
        return 'No Response'
    
def getresponse():
    keyword=input("Enter keyword for twitter: ")
    country=input("enter country for twitter: ")
    
    keyword += '/' + country
        
    print(f'\n Fetching tweets for- {keyword} \n')

    df_twitter=twitter_search(keyword)
    top_influencers = influencers_twitter(keyword)

    print(f'\n Top 20 Influencers for {keyword}: \n\n', top_influencers)

    print(df_twitter)

    return df_twitter

#getresponse()
