import tweepy
import ast
import json
import bs4
import atexit
import requests

#override tweepy.StreamListener to add logic to on_status
tweets = {}
#soup = bs4.BeautifulSoup()

def get_article(url):
	if url=="":
		return ""
	r = requests.get(url)
	print "Expanded text"
	print r.text
	return r.text

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
    	tweet = json.loads(data)
    	url = ""
    	if "urls" in tweet["entities"]:
    		if "expanded_url" in tweet["entities"]["urls"][0]:
    			url = tweet["entities"]["urls"][0]["expanded_url"]
    			print url
    	#print tweet["id_str"]
    	self.tweets[tweet["id_str"]]={"text":tweet["text"],"user":tweet["user"]["screen_name"],"url":url,"expanded_text":get_article(url)}
    	#print str(self.id)+" "+str(len(self.tweets))
    	if len(self.tweets)%50==0:
    		print "--------------------"
    		print self.id
    		#print self.tweets
    	return True

    def on_error(self, status):
    	print "Error"
        print(status)

    def get_tweets(self):
    	return self.tweets

    def __init__(self, num):
		self.tweets = {}
		self.id = num


