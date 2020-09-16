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
author.append(soup.find(attrs={'class': matchAuthor}))
print(first(author))

def parse(url, file):
	pass
	# return keys
	# meta tag search
	# search for all elements within body that:
		# contain inner text with at least one space and a number of characters in some range
		# contain text even when excluding children and just one element in it
		# number of direct children
		# number of total children
		# max children depth
		# tag names of self or any children don't include canvas, iframe, img, style, script, video
		# offsetHeight
		# offsetTop
		# TODO font size and styling

# Array.from(document.body.querySelectorAll('*')).filter(i =>
# 	i.innerText &&
# 	i.childNodes[0].nodeValue &&
# 	i.children.length < 5 &&
# 	i.querySelectorAll('*').length < 10 &&
# 	i.querySelectorAll('canvas,iframe,img,style,script').length == 0 &&
# 	i.getBoundingClientRect().width > 16 &&
# 	i.getBoundingClientRect().width < 800 &&
# 	i.getBoundingClientRect().height > 8 &&
# 	i.getBoundingClientRect().height < 100 &&
# 	i.getBoundingClientRect().top > 0 &&
# 	i.getBoundingClientRect().top < 2000 &&
# 	i.getBoundingClientRect().bottom > 0 &&
# 	i.getBoundingClientRect().left > 0 &&
# 	i.getBoundingClientRect().right > 0
# )