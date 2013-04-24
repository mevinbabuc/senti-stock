#! /usr/bin/python

#Application To Retrieve Real Time Data From The Net For Each Company
#Version 1.0 ( Database Storage )
#Coderx13

import json,urllib2,MySQLdb,re,datetime,pytz,os,threading
from time import sleep
from pytz import timezone

OPENSHIFT_LOG_DIR = os.getenv("OPENSHIFT_PYTHON_LOG_DIR") 

import logging
FORMAT='%(asctime)-15s %(message)s'
logging.basicConfig(filename=OPENSHIFT_LOG_DIR+"error_insider.log",level=logging.DEBUG,format=FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

logging.info('Insider initialized')

#RealTime InsideStock Prediction Collector
class InsideStockPredictionCollector(threading.Thread):

    #Class Constructor
	def __init__(self, Company):

		self.Company = Company
		self.cnx=None
		self.flag=None
		threading.Thread.__init__(self)
		# self.daemon = True

	def run(self):
		if(self.Company=="bac"):
			response="http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.insidestocks.com%2Ftexpert.asp%3Fcode%3DBAHT%26sym%3DBAC%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fcenter%5B1%5D%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%2Ftd%5B2%5D%2Ftable%5B3%5D%2Ftr%5B5%5D%2Ftd%5B3%5D%2Fp'&format=json&callback="
			self.flag=1
		elif(self.Company=="aapl"):
			response="http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.insidestocks.com%2Ftexpert.asp%3Fcode%3DBAHT%26sym%3DAAPL%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fcenter%5B1%5D%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%2Ftd%5B2%5D%2Ftable%5B3%5D%2Ftr%5B5%5D%2Ftd%5B3%5D%2Fp'&format=json&callback="
		elif(self.Company=="goog"):
			response="http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D'http%3A%2F%2Fwww.insidestocks.com%2Ftexpert.asp%3Fcode%3DBAHT%26sym%3DGOOG'%20and%20xpath%3D'%2Fhtml%2Fbody%2Fcenter%5B1%5D%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%2Ftd%5B2%5D%2Ftable%5B3%5D%2Ftr%5B5%5D%2Ftd%5B3%5D%2Fp'&format=json&diagnostics=true&callback="
		try:			
			config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
			self.cnx = MySQLdb.connect(**config)
			logging.info("Getting prediction For %s."%self.Company)
			add_prediction = "INSERT ignore INTO prediction_%s (decision,time)VALUES (%s,%s)"
			obj= json.load(urllib2.urlopen(response))
			content ="'"+re.sub(r"'|\"", "",str(obj['query']['results']['p']))+"'"
			cur=self.cnx.cursor()	
			d = datetime.datetime.today()	
			america=timezone('America/New_York')
			india=timezone('Asia/Kolkata')
			dd=america.localize(d)
			dd=dd.astimezone(india)	
			cur.execute(add_prediction%(self.Company,content,"'"+dd.strftime('%Y-%m-%d')+"'"))
			self.cnx.commit()
		except Exception as e :
			if(self.flag==1):
				response="http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D'http%3A%2F%2Fwww.insidestocks.com%2Ftexpert.asp%3Fcode%3DBAHT%26sym%3DBAC'%20and%20xpath%3D'%2Fhtml%2Fbody%2Fcenter%5B1%5D%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%2Ftd%5B2%5D%2Ftable%5B3%5D%2Ftr%5B5%5D%2Ftd%5B2%5D%2Fp'&format=json&callback="
				self.flag=2
			elif(self.flag==2):
				self.flag=1
				response="http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.insidestocks.com%2Ftexpert.asp%3Fcode%3DBAHT%26sym%3DBAC%22%20and%20xpath%3D'%2Fhtml%2Fbody%2Fcenter%5B1%5D%2Ftable%2Ftr%2Ftd%2Ftable%5B2%5D%2Ftr%2Ftd%5B2%5D%2Ftable%5B3%5D%2Ftr%5B5%5D%2Ftd%5B3%5D%2Fp'&format=json&callback="
				logging.info("Error : "+str(type(e))+str(e))
			else :
				logging.info("Prediction Added To Database For %s."%self.Company)
				# del obj
		self.cnx.close()




#main
print "Threads started!"

#InsideStockPredictions Collection
bacPrediction=InsideStockPredictionCollector("bac")
bacPrediction.start()
aaplPrediction=InsideStockPredictionCollector("aapl")
aaplPrediction.start()
googPrediction=InsideStockPredictionCollector("goog")
googPrediction.start()

# sleep(2000)
logging.info("Insider : collection stopped")