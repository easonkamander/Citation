from bs4 import BeautifulSoup
import functools
import operator
import requests
import sys
import re

first = lambda xs: functools.reduce(lambda x, y: x or y, xs, False)

def crawl(url):
        page = requests.get(url)
        return BeautifulSoup(page.text, 'lxml')

url = sys.argv[1]
soup = crawl(url)
matchMeta = re.compile('author')
author = [soup.find('meta', attrs={'name':matchMeta})]
matchAuthor = re.compile('author.*byline|byline.*author|author-name|authorName', re.IGNORECASE)
author.append( soup.find(attrs={'class': matchAuthor}) )
print(first(author))