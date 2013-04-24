#! /usr/bin/python

import urllib2,json,threading,MySQLdb,re,datetime,pytz,os
from time import sleep
from pytz import timezone

OPENSHIFT_LOG_DIR = os.getenv("OPENSHIFT_PYTHON_LOG_DIR") 

import logging
FORMAT='%(asctime)-15s %(message)s'
logging.basicConfig(filename=OPENSHIFT_LOG_DIR+"error_searchTwit.log",level=logging.DEBUG,format=FORMAT,datefmt="%Y-%m-%d %H:%M:%S")

logging.info('SearchTwit initialized')

class NewsCollector(threading.Thread):
	
    #Class Constructor
    def __init__(self, Company):
        
        self.Company = Company
        self.C="%s since:"%Company
        threading.Thread.__init__(self)
        self.daemon = True
 

    def run(self):
        config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
        self.cnx = MySQLdb.connect(**config)
        if(self.Company=="$BAC"):
            self.tbl="bac"
        elif(self.Company=="$AAPL"):
            self.tbl="aapl"
        elif(self.Company=="$GOOG"):
            self.tbl="goog"
        add_tweet = "INSERT ignore INTO tweets_%s (tweet,time)VALUES (%s,%s)"
        counter = 1 ;
        while True:
            try:
                self.Query=urllib2.quote(self.C+str(datetime.date.today().isoformat()))
                if(self.cnx==None):
                    logging.info("Trying to connect")
                    self.cnx = MySQLdb.connect(**config)	
                for i in range(1,16):
                    link='http://search.twitter.com/search.json?q="'+self.Query+'"'+'&&lang=en&&page='+str(i)+'&&rpp=100'
                    jsonobj=json.loads(urllib2.urlopen(link).read())
                    for tweet in jsonobj["results"]:
                        try:
                            content = str(re.sub(r"'|\"|(@[A-Za-z0-9]+)|(\w+:\/\/\S+)|(#[^ ]+)|(RT : )", "",tweet["text"].encode("utf-8")))
                            cur=self.cnx.cursor()
                            d = datetime.datetime.today()
                            america=timezone('America/New_York')
                            india=timezone('Asia/Kolkata')
                            dd=america.localize(d)
                            dd=dd.astimezone(india)
                            #print add_tweet%(self.tbl,"'"+content+"'","'"+d.ctime()+"'")
                            cur.execute(add_tweet%(self.tbl,"'"+content+"'","'"+dd.strftime('%Y-%m-%d %H:%M:%S')+"'"))
                            self.cnx.commit()
                            counter+=1
                            logging.info(self.Company+" tweet added "+str(counter)+" ")
                        except MySQLdb.IntegrityError:
                            logging.info("Error,Tweet has already been added")
            except Exception as e :
                logging.info(str(e))
            sleep(60)



logging.info("Search : Tweet collection started")

googPrediction=NewsCollector("$GOOG")
googPrediction.start()
bacPrediction=NewsCollector("$BAC")
bacPrediction.start()
aaplPrediction=NewsCollector("$AAPL")
aaplPrediction.start()


sleep(2500)
logging.info("Search : Tweet collection stopped")
