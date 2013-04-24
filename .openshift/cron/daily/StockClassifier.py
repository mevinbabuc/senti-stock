#! /usr/bin/python

#Threaded tweet classifier
#mevinbabuc@gmail.com

import MySQLdb,threading,datetime,pytz,os,PyClassi,gc
from time import sleep
from pytz import timezone


OPENSHIFT_LOG_DIR = os.getenv("OPENSHIFT_PYTHON_LOG_DIR")

import logging
FORMAT='%(asctime)-15s %(message)s'
logging.basicConfig(filename=OPENSHIFT_LOG_DIR+"error_classifier.log",level=logging.DEBUG,format=FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

logging.info('Classifier initialized')

#close unnecessary connections
gc.collect()

#RealTime Stock Collector
class StockClassifier(threading.Thread):

	#Class Constructor
	def __init__(self, Company):

		self.Company = Company
		self.cnx=None
		threading.Thread.__init__(self)

	#Function To Store Realtime Stock in The Database
	def run(self):
		config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'backup'}
		self.cnx = MySQLdb.connect(**config)
		logging.info("Classifying For %s."%self.Company)
		neg_count=0
		pos_count=0
		try:
			if(self.cnx==None):
				self.cnx = MySQLdb.connect(**config)

			d = datetime.datetime.today()
			america=timezone('America/New_York')
			india=timezone('Asia/Kolkata')
			dd=america.localize(d)
			dd=dd.astimezone(india)

			get_tweet = "select * from tweets_"+self.Company+" where sentiment!=1"
			cur=self.cnx.cursor()
			cur.execute(get_tweet)
			db_tweets = cur.fetchall()

			for line in db_tweets:
				value=PyClassi.classify(line[1],self.Company)

				if value==0:
					neg_count+=1
				elif value==2:
					pos_count+=1

				update="update tweets_"+self.Company+" set classified="+str(value)+" where id="+str(line[0])
				cur.execute(update)

			sen_value=float(pos_count)/neg_count

			add_Stock = "INSERT ignore INTO bay_%s VALUES (%s,%s)"
			cur.execute(add_Stock%(self.Company,"'"+str(sen_value)+"'","'"+dd.strftime('%Y-%m-%d')+"'"))
			self.cnx.commit()

		except Exception as e :
			logging.info(self.Company+"Error : "+str(type(e))+str(e))
		else :
			logging.info(self.Company+"Bayesian value Added To Database For %s."%self.Company)
		self.cnx.close()

# Stock Collection
bacStock=StockClassifier("bac")
bacStock.start()
aaplStock=StockClassifier("aapl")
aaplStock.start()
googStock=StockClassifier("goog")
googStock.start()

logging.info("Stock : Classification stopped")