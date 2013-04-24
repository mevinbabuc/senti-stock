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
logging.basicConfig(filename=OPENSHIFT_LOG_DIR+"error_news.log",level=logging.DEBUG,format=FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

logging.info('News initialized')

#RealTime News Collector
class NewsCollector(threading.Thread):

	#Class Constructor
	def __init__(self, Company):

		self.Company = Company
		self.cnx=None
		threading.Thread.__init__(self)
		self.daemon = True

	#Function To Store Realtime News in The Database
	def run(self):
		config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
		self.cnx = MySQLdb.connect(**config)
		logging.info("Getting News For %s."%self.Company)
		while True:
			try:
				if(self.cnx==None):
					self.cnx = MySQLdb.connect(**config)
				d = datetime.datetime.today()
				america=timezone('America/New_York')
				india=timezone('Asia/Kolkata')
				dd=america.localize(d)
				dd=dd.astimezone(india)
				add_news = "INSERT ignore INTO news_%s (content,href,time)VALUES (%s,%s,%s)"
				if(self.Company=="bac"):
					response="http://query.yahooapis.com/v1/public/yql?q=select%20href%2Ccontent%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fh%3Fs%3DBAC%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fdiv%5B4%5D%2Fdiv%5B4%5D%2Ftable%5B2%5D%2Ftr%2Ftd%2Ftable%2Ftr%2Ftd%2Fdiv%2Ful%2Fli%2Fa'&format=json"
				elif(self.Company=="aapl"):
					response="http://query.yahooapis.com/v1/public/yql?q=select%20href%2Ccontent%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fh%3Fs%3DAAPL%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fdiv%5B4%5D%2Fdiv%5B4%5D%2Ftable%5B2%5D%2Ftr%2Ftd%2Ftable%2Ftr%2Ftd%2Fdiv%2Ful%2Fli%2Fa'&format=json"
				elif(self.Company=="goog"):
					response="http://query.yahooapis.com/v1/public/yql?q=select%20href%2Ccontent%20from%20html%20where%20url%3D%22http%3A%2F%2Ffinance.yahoo.com%2Fq%2Fh%3Fs%3DGOOG%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fdiv%5B4%5D%2Fdiv%5B4%5D%2Ftable%5B2%5D%2Ftr%2Ftd%2Ftable%2Ftr%2Ftd%2Fdiv%2Ful%2Fli%2Fa'&format=json"
				obj= json.load(urllib2.urlopen(response))
				content =  "'"+re.sub(r"'|\"", "", str(obj['query']['results']['a'][0]['content'])).encode('utf-8')+"'"
				href =  "'"+urllib2.quote(re.sub(r"'|\"", "", str(obj['query']['results']['a'][0]['href'])).encode('utf-8'))+"'"
				cur=self.cnx.cursor()
				cur.execute(add_news%(self.Company,content,href,"'"+dd.strftime('%Y-%m-%d %H:%M:%S')+"'"))
				self.cnx.commit()
			except  MySQLdb.IntegrityError :
				logging.info("News Already Added For "+self.Company+", Will Try After 1 minutes.")
				sleep(60)
			except Exception as e :
				logging.info("Error : "+str(type(e))+str(e))
			else :
				logging.info("News Added To Database For %s."%self.Company)
				del obj
		self.cnx.close()

# News Collection
bacNews=NewsCollector("bac")
bacNews.start()
aaplNews=NewsCollector("aapl")
aaplNews.start()
googNews=NewsCollector("goog")
googNews.start()

sleep(2000)
logging.info("News : collection stopped")