#! /usr/bin/python

#Application To Retrieve Real Time Data From The Net For Each Company
#Version 1.0 ( Database Storage )
#Coderx13

import json,urllib2,MySQLdb,re,threading,datetime,pytz,os
from time import sleep
from pytz import timezone

OPENSHIFT_LOG_DIR = os.getenv("OPENSHIFT_PYTHON_LOG_DIR") 

import logging
FORMAT='%(asctime)-15s %(message)s'
logging.basicConfig(filename=OPENSHIFT_LOG_DIR+"error_Quotes.log",level=logging.DEBUG,format=FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

logging.info('Quotes initialized')

#Realtime quote collector
class QuoteCollector(threading.Thread):
    
	#Class Constructor
	def __init__(self, Company):

		self.Company = Company
		self.cnx=None
		threading.Thread.__init__(self)
		# self.daemon = True


	#Function To Store Realtime Quotes in The Database
	def run(self):
		config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
		self.cnx = MySQLdb.connect(**config)
		# while True:
		try:
			if(self.cnx==None):
				self.cnx = MySQLdb.connect(**config)
			logging.info("Getting Quote For %s."%self.Company)
			add_quotes = "INSERT INTO quotes_%s (quote,time)VALUES (%s,%s)"
			if(self.Company=="bac"):
				response="http://query.yahooapis.com/v1/public/yql?q=select%20content%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fh%3Fs%3DBAC%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fdiv%5B3%5D%2Fdiv%5B4%5D%2Fdiv%2Fdiv%2Fdiv%2Fdiv%2Fdiv%5B2%5D%2Fp%2Fspan%5B1%5D%2Fspan'&format=json"
			elif(self.Company=="aapl"):
				response="http://query.yahooapis.com/v1/public/yql?q=select%20content%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fh%3Fs%3DAAPl%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fdiv%5B3%5D%2Fdiv%5B4%5D%2Fdiv%2Fdiv%2Fdiv%2Fdiv%2Fdiv%5B2%5D%2Fp%2Fspan%5B1%5D%2Fspan'&format=json&callback="
			elif(self.Company=="goog"):
				response="http://query.yahooapis.com/v1/public/yql?q=select%20content%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fh%3Fs%3DGOOG%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fdiv%5B3%5D%2Fdiv%5B4%5D%2Fdiv%2Fdiv%2Fdiv%2Fdiv%2Fdiv%5B2%5D%2Fp%2Fspan%5B1%5D%2Fspan'&format=json&callback="
			obj= json.load(urllib2.urlopen(response))
			content =  "'"+re.sub(r"'|\"", "", str(obj['query']['results']['span']))+"'"
			cur=self.cnx.cursor()
			d = datetime.datetime.today()
			america=timezone('America/New_York')
			india=timezone('Asia/Kolkata')
			dd=america.localize(d)
			dd=dd.astimezone(india)
			cur.execute(add_quotes%(self.Company,content,"'"+dd.strftime('%Y-%m-%d %H:%M:%S')+"'"))
			self.cnx.commit()
		except Exception as e :
			logging.info("Error : "+str(type(e))+str(e))
		else :
			logging.info("Quote Added To Database For %s."%self.Company)
			del obj
		self.cnx.close()


#main
print "Threads started!"

#Quote Collection
bacQuote=QuoteCollector("bac")
bacQuote.start()
aaplQuote=QuoteCollector("aapl")
aaplQuote.start()
googQuote=QuoteCollector("goog")
googQuote.start()
logging.info("Quotes : collection stopped")