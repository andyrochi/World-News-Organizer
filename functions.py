import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as BS
from pytrends.request import TrendReq
from newsapi import NewsApiClient

def get_news(newsapi,source_num):
    news_list = list()
    source_dict = {
        '1' : 'the-new-york-times',
        '2' : 'time',
        '3' : 'reuters',
        '4' : 'bbc-news',
        '5' : 'the-wall-street-journal',
        '6' : 'associated-press',
        '7' : 'al-jazeera-english',
        '8' : 'cnn'
    }
    try:
        source = source_dict[source_num]
    except KeyError:
        print('News source key error, please check funtions.py')
        exit()
    
    top_headlines = newsapi.get_top_headlines(sources=source)
    
    number_of_headlines = 3
    if len(top_headlines['articles']) < number_of_headlines:
        number_of_headlines = len(top_headlines['articles'])
    
    for i in range(number_of_headlines):
        data = dict()

        headline_set = top_headlines['articles'][i]
        author = headline_set['author']
        title = headline_set['title']
        description = headline_set['description']
        url = headline_set['url']
        image = headline_set['urlToImage']

        #replace apostrophes with escape sequence
        title = title.replace("’","&#8217").replace("'","&#39").replace("—","&#8212").replace("–","&#8211")
        description = description.replace("’","&#8217").replace("'","&#39").replace("—","&#8212").replace("”","&#8221").replace("“","&#8220").replace("–","&#8211")   
        
        #grab keywords
        if source_num == '1':
            keywords = keywords_nyt(url)
        elif source_num == '2':
            keywords = keywords_time(url)
        elif source_num == '3':
            keywords = keywords_reuters(url)
        elif source_num == '4':
            keywords = keywords_bbc(url)
        elif source_num == '5':
            keywords = keywords_wsj(url)
        elif source_num == '6':
            keywords = keywords_associatedpress(url)
        elif source_num == '7':
            keywords = keywords_aljazeera(url)
        else:
            keywords = keywords_cnn(url)
        
        data['title'] = title
        data['description'] = description
        data['url'] = url
        data['image'] = image
        data['author'] = author
        data['keywords'] = keywords[:5]
        print('Getting related topics...')
        data['related'] = related_topics(data['keywords'])

        news_list.append(data)
    return news_list

def keywords_aljazeera(url):
    """
    Pass url into function
    Crawl news keywords from aljazeera news page with url
    """
    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    keywords_tag = soup.find("meta", {"name" : "news_keywords"})
    keywords_string = keywords_tag['content']
    keywords = keywords_string.split(',')
    
    return keywords

def keywords_nyt(url):
    """
    Pass url into function
    Crawl news keywords from nyt page with url
    """

    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    keywords_tag = soup.find("meta", {"name" : "news_keywords"})
    keywords_string = keywords_tag['content']
    keywords = keywords_string.split(',')
    
    return keywords

def keywords_time(url):
    """
    Pass url into function
    Crawl news keywords from time page with url
    """

    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    keywords_tag = soup.find("meta", {"name" : "news_keywords"})
    keywords_string = keywords_tag['content']
    keywords = keywords_string.split(',')

    return keywords

def keywords_reuters(url):
    """
    Pass url into function
    Crawl news keywords from Reuters page with url
    """
    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    keywords_tag = soup.find("meta", {"name" : "news_keywords"})
    keywords_string = keywords_tag['content']
    keywords = keywords_string.split(';')

    return keywords

def keywords_bbc(url):
    """
    Pass url into function
    Crawl news keywords from BBC page with url
    """
    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    tags = soup.find_all(class_="tags-list__tags")
    keywords = list()
    for tag in tags:
        keyword = tag.text
        keywords.append(keyword)

    return keywords

def keywords_wsj(url):
    """
    Pass url into function
    Crawl news keywords from BBC page with url
    """
    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    keywords_tag = soup.find("meta", {"name" : "news_keywords"})
    keywords_string = keywords_tag['content']
    keywords_before = keywords_string.split(',')

    #filter useless keywords
    def useless(x):
        if 'exclusive' in x:
            return True
        elif 'general news' in x:
            return True
        else:
            return False

    keywords = [x for x in keywords_before if not useless(x)]
    return keywords

def keywords_associatedpress(url):
    #grab keywords
    html = urllib.request.urlopen(url)
    soup = BS(html,'html.parser')
    tags = soup.find_all(attrs={"data-key": "related-tag"})
    keywords = list()
    for tag in tags:
        keyword = tag.text
        #bypass unusful keywords
        if keyword == "AP Top News" or keyword == "International News" or keyword == "General News":
            continue
        keywords.append(keyword)

    return keywords

def keywords_cnn(url):
    #grab keywords
    html = urllib.request.urlopen(url)
    print("Retrieving from url:",url)
    soup = BS(html,'html.parser')
    keywords_tag = soup.find("meta", {"name" : "keywords"})
    keywords_string = keywords_tag['content']
    keywords = list()
    keywords.append(keywords_string.split(',')[0])

    return keywords

def related_topics(keywords):
    """
    Usage: Return a dictionary of strings(related topics) for each keyword

    """
    related_topics_dict = dict()
    for keyword in keywords:
        kwlist = [keyword]

        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        pytrends.build_payload(kwlist)
        
        #Prevent pytrend fail
        try:
            data = pytrends.related_topics()
        except:
            related_string = 'Related Topics: None'
            related_topics_dict[keyword] = related_string
            continue
        print(keyword)
        #print(data)
        
        for x in data:
            key = x
            break
        
        df = data[key]['top']
        
        #Error exception
        IsDataEmpty = df.empty
        if IsDataEmpty == True:
            related_string = 'Related Topics: None'
        else:
            related_topics_list = []
            related_topics_list.append('Related topics:')
            
            #top 4 related topics
            for i in range(1,5):
                try:
                    item = str(i)+'.' + df.at[i,'topic_title']
                    related_topics_list.append(item)
                except KeyError:
                    break
            
            related_string = ' '.join(related_topics_list)
        related_topics_dict[keyword] = related_string

    return related_topics_dict
        