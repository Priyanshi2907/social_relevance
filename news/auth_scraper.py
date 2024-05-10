import google.generativeai as genai
    

GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'

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
        # ,seperated by comma and without numbering and any symbol

    try:
        
        response = model.generate_content(f"""
  
            You are a helpful assistant that will help me in finding the Top 10 Related words for the following Keyword: {keyword}
            in the form of  list in a single line ,seperated by comma and and don't list the words with any numbering or any symbol at the starting of the topic,only give the words

            
          
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
  
            You are a helpful assistant that will help me in finding the min Top 10 Trending Topics for the following Keyword: {keyword}                        
             ,in the form of list in a single line and don't make the list with any numbering or any symbol at the starting of the topic,only give the topic
            """)

        return response.text
        
    except Exception as e:
        print(e)
        return 'No Response'
    
def take_keyword():
    keyword = input("Enter keyword: ")
    country= input("Enter Country : ")
    keyword += ' ' + country
        
    print(f'\n Fetching related keyword,authors , topics   for- {keyword} \n')
    #news_data = google_news_scraper(keyword)
    
    relatedwords = relatedwords_news(keyword)
    #authors = authors_news(keyword)
    Trending_topics = Trending_topics_news(keyword)

    print(f'\n Top 10 Related Words for {keyword}: \n\n', relatedwords)
    #print("Top 10 Authors for {keyword}:", authors)
    print("Top trending topics for {keyword}:", Trending_topics)


    #df = pd.DataFrame(news_data)
    #print(df)

#take_keyword()
# def authors_news(keyword):
#     """
#     Fetches Top  Authors for the given keyword
#     """
#     try:
        
#         response = model.generate_content(f"""
  
#             You are a helpful assistant that will help me in finding the  Top 10 authors for the following Keyword: {keyword}
#             ,in the form of list in a single line and without numbering and any symbol
            
            
#             """)

#         return response.text
        
#     except Exception as e:
#         print(e)
#         return "No response"
