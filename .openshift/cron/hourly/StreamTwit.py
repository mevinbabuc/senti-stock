#! /usr/bin/python

#Application To Retrieve Real Time Data From The Net For Each Company
#Version 1.0 ( Database Storage )
#Coderx13

import json,urllib2,MySQLdb,re,threading,tweetstream,datetime,pytz,os
from time import sleep
from pytz import timezone

OPENSHIFT_LOG_DIR = os.getenv("OPENSHIFT_PYTHON_LOG_DIR") 

import logging
FORMAT='%(asctime)-15s %(message)s'
logging.basicConfig(filename=OPENSHIFT_LOG_DIR+"error_StreamTwit.log",level=logging.DEBUG,format=FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

logging.info('StreamTwit initialized')

class TweetCollector(threading.Thread):
	
	#Class Constructor
	def __init__(self, Company):

		threading.Thread.__init__(self)
		self.daemon = True
		self.words = []				
		self.Company=Company
		self.words.append(Company)
		self.cnx=None
		self.usr=None
		self.pss=None
		self.tbl=None

	#Function To Store Realtime Tweets in The Database
	def run(self):
		config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
		self.cnx = MySQLdb.connect(**config)

		if(self.Company=="$BAC"):
			self.usr="jovin2010"
			self.pss="blublu"
			self.tbl="bac"
		elif(self.Company=="$AAPL"):
			self.usr="sentiaapl"
			self.pss="rohit123rv"
			self.tbl="aapl"
		elif(self.Company=="$GOOG"):
			self.usr="googsenti"
			self.pss="rohit123rv"
			self.tbl="goog"
		while True:
			try:
				Retweet = ['RT']
				if(self.cnx==None):
					logging.info("Trying to connect")
					self.cnx = MySQLdb.connect(**config)
				cur=self.cnx.cursor()
				add_tweet = "INSERT ignore INTO tweets_%s (tweet,time)VALUES (%s,%s)"
				with tweetstream.FilterStream(self.usr, self.pss,track=self.words) as stream:
					logging.info("Connected To Twitter Stream For %s Successfully."%self.Company)
					for tweet in stream:
						if 'text' not in tweet: continue
						tweet_data = re.sub(r"'|\"", "",tweet['text'].encode('UTF-8'))
						if any(word in tweet_data for word in Retweet): continue
						new_tweet_data=re.sub(r"'|\"", "",tweet_data)
						d = datetime.datetime.today()
						america=timezone('America/New_York')
						india=timezone('Asia/Kolkata')
						dd=america.localize(d)
						dd=dd.astimezone(india)
						print tweet_data
						cur.execute(add_tweet % (self.tbl,("'"+new_tweet_data+"'"),"'"+dd.strftime('%Y-%m-%d %H:%M:%S')+"'"))
						logging.info("Tweet Added For %s."%self.Company)
						self.cnx.commit()
			except Exception as e:
				logging.info("Connection To Twitter For %s Has Encountered An Error, Reconnecting.."%self.Company+" "+str(e))
				sleep(60)


#main
print "Threads started!"

#Tweets Collection
googTweet=TweetCollector("$GOOG")
googTweet.start()
bacTweet=TweetCollector("$BAC")
bacTweet.start()
aaplTweet=TweetCollector("$AAPL")
aaplTweet.start()

sleep(2000)

logging.info("StreamTwit : collection stopped")