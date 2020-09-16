import requests

def crawl(url):
	return requests.get(url).text