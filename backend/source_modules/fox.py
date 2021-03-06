'''
Author: Daniel Frederick
Date: May 21, 2020

fox news site specific web scraper
'''

'''
PASTEBIN

'''

from lxml import html
import requests
import json

url = 'https://www.foxnews.com/'

    # exports standardized articles from query
    # query - string - search term
class FoxQuery:
    def __init__(self, query):
        self.query = query
        # list of article objects
        self.result_articles = self.getResultArticles()

    def getResultArticles(self):
        query_url_front = 'https://api.foxnews.com/search/web?q='
        query_url_back = '+more:pagemap:metatags-pagetype:article+more:pagemap:metatags-dc.type:Text.Article&siteSearch=foxnews.com&siteSearchFilter=i&callback=__jp2'
        # --- get list of articles
        query_url = str(query_url_front) + str(self.query) + str(query_url_back)
        query_json = requests.get(query_url).content
        # format json so it can be parsed
        query_json = query_json.decode('utf-8')[22:-3]
        # parse json so it can be used as a dictionary
        parsed_query_json = json.loads(query_json)
        # get array of result article objects
        results = parsed_query_json['items']
        articles = []
        # loop through results and pick out articles only, then create an article instance and add it to an array
        for i in results:
            metatags = i['pagemap']['metatags'][0]
            article = Article(i['link'], metatags)
            articles.append(article)
        return articles
    

    # article class
class Article:
    def __init__(self, url, metatags):
        # dictionary of metatags
        self.metatags = metatags
        self.url = url
        self.title = metatags["dc.title"]
        self.desc = metatags["dc.description"]
        self.date = metatags["dc.date"]
        self.image = metatags["og:image"]
        # self.author = metatags["dc.creator"]
        self.article_content = self.getArticleContent()

        self.info = 'Source : ABC News\nTitle: {}\nDescription: {}\nDate Published: {}\nURL: {}'.format(self.title,  self.desc, self.date, self.url)

    # returns a string of article content
    def getArticleContent(self):
        article_page =  requests.get(self.url)
        article_tree = html.fromstring(article_page.content)

        article_content_p_list = article_tree.xpath('//div[@class="article-content"]//p')
        article_content = '' 
        for i in article_content_p_list:
            article_content = article_content + i.text_content()
        
        return article_content