import google.generativeai as genai
    

GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'


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
    Fetches Top Influencers ,Hashtags ,Top trending Topics for the given keyword
    """
    try:

        response = model.generate_content(f"""
  
             You are a helpful assistant that will help me in finding the Top 10 Influencers with thier name and clickable twitter profile links for the following Keyword: {keyword}
            in a format for example ["Name of Influencer 1" : "Twitter link" , "Name of Influencer 2" : "Twitter link" and so on], without numbering  and without "\"  and should be in a single line            """)

        return response.text
        
    except Exception as e:
        print(e)
        return 'No Response'

def Hashtags_twitter(keyword):
    """
    Fetches Top Hashtags  for the given keyword
    """
    try:

        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the Top 10 Trending Hashtags  for the following Keyword: {keyword}                        
            seperated by only space,in the form of list,in a single line
            
            """)

        return response.text
        
    except Exception as e:
        print(e)
        return 'No Response'

def Trending_topics_twitter(keyword):
    """
    Fetches Top Trending topics  for the given keyword
    """
    try:

        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the Top Trending Topics for the following Keyword: {keyword}                        
            ,in the form of list, in a single line, only the topics without any symbol and numbering
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

    #df_twitter=twitter_search(keyword)
    top_influencers = (influencers_twitter(keyword))
    top_hashtags = (Hashtags_twitter(keyword)).split(' ')
    top_trending_topics = (Trending_topics_twitter(keyword)).split(' ')

    
    print(f'\n Top 10 Influencers for {keyword}: \n\n', top_influencers)    
    print(f'\n Top 10 Hashtags for {keyword}: \n\n', top_hashtags)
    print(f'\n Top 10 tt for {keyword}: \n\n', top_trending_topics)


    #print("Top 10 Hashtags for {keyword}:", (top_hashtags))
    #print("Top trending topics for {keyword}:", top_trending_topics)


    # print(df_twitter)

    # return df_twitter

#getresponse()
