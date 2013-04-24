#! /usr/bin/python

from re import sub,compile
from nltk import stem
from Queue import Queue
import limits,MySQLdb,threading,gc,csv,cPickle as pickle,PyNegator as neg#,SpellCheck as sp
from collections import defaultdict

direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/bigdata/"
out_dir="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/smalldata/"

#close unnecessary connections
gc.collect()

# tweet_filter=compile(r"[\\]|[()]|[)]|[\"]|[']|[,]|[!]|[.]|[#][^ ]+|[&]|[-]|[?]|[_]|((http|https)://)[^ ]+|\w*[@][^ ]+|\b[\S0-9]\b|\b[0-9]+\b")
tweet_filter=compile(r"[\\]|[()]|[)]|[\"]|[']|[,]|[!]|[.]|[#][^ ]+|[$][^ ]+|[&]|[-]|[?]|[_]|((http|https)://)[^ ]+|\w*[@][^ ]+|\b[\S0-9]\b|\b[0-9]+\b")

#remove repeating charecters
word_normalize=compile(r'(\w)\1+')

#load stop words
stop=pickle.load(open(direct+"stopwords.blu",'rb')) 

#load synonym words
dicSyn=pickle.load(open(direct+"synonym.blu",'rb')) 

#load spell check words
dicSpell=pickle.load(open(direct+"spell.blu",'rb')) 

#splits the data in files into lines and inserts them into work Queue
workq=Queue()

def make_Queue(filename):
    config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
    cnx = MySQLdb.connect(**config)
    
    cur=cnx.cursor()
    get_neg_tweet = "select * from tweets_aapl where sentiment=2 union select * from tweets_bac where sentiment=2 union select * from tweets_goog where sentiment=2"
    cur.execute(get_neg_tweet)
    
    db_tweets = cur.fetchall()
    
    for line in db_tweets:
        lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
        workq.put(lne)
        
    cnx.close()

#extract bi-gram features and places them in Queues for word counting
processq=Queue()


class ThreadExtract(threading.Thread):

    def __init__(self,workq,processq,id):
        threading.Thread.__init__(self)
        self.workq=workq
        self.processq=processq
        self.id=id

    def filter(self,word):

    	# Spell check
    	if dicSpell.has_key(word):
                    word=dicSpell[word]
    	# Stem the words
    	WordStem=stem.PorterStemmer().stem(word)

    	# if WordStem in stop:
    	# 	WordStem=""
    	# else :
	    	# Synonym replacement
    	if dicSyn.has_key(WordStem):
    		WordStem=dicSyn[WordStem]

    	return WordStem.strip()
        
    def run(self):

        while True :
            tuple=self.workq.get()
            
            #Convert tweet into a list of words
            feature=list(tuple.split())

            for word in range(0,len(feature)-1):
                bigram=self.filter(feature[word])+" "+self.filter(feature[word+1])
                
                # Antonym replacer
                # bigram=neg.replace_negations(bigram)

                self.processq.put(bigram)
            self.workq.task_done()


Bigramdic=defaultdict(int)
Unigramdic=defaultdict(int)
lock=threading.RLock()

#count the word frequency
class ThreadFreq(threading.Thread):
    
    def __init__(self,processq,id):
        threading.Thread.__init__(self)
        self.processq=processq
        self.id=id
    
    def run(self):
        while True:
            bigram=processq.get()
            BiList=bigram.split()
            #print BiList
            if len(BiList) >1:
                with lock:
                    Bigramdic[bigram.strip()]+=1
                    for unigram in BiList:
                        if unigram.strip()!='' :
                            Unigramdic[unigram.strip()]+=1
            else :
                if bigram.strip()!='' :
                    with lock:
                        Unigramdic[bigram.strip()]+=1
            #print self.processq.qsize()
            self.processq.task_done()


#Thread Generation !

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(workq,processq,i)
    t.setDaemon(True)
    t.start()

print "started filling the queue"
make_Queue("positive.txt")
print "Queue full"

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(processq,i)
    tf.setDaemon(True)
    tf.start()

#Waiting for the Threads!

workq.join()
processq.join()

# Frequency Filtering

posbidic=defaultdict(int)
posunidic=defaultdict(int)

for word in Bigramdic:
    tmp=Bigramdic[word]
    if tmp > limits.BI_Threshold:
        posbidic[word]=tmp

for word in Unigramdic:
    tmp=Unigramdic[word]
    if tmp > limits.UNI_Threshold:
        posunidic[word]=tmp

with open(direct+'pos_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in posunidic:
            posunidic[row[0]]+=(float)(row[1])        

pickle.dump(posbidic,open(out_dir+"Bipositive.p",'wb'))
pickle.dump(posunidic,open(out_dir+"Unipositive.p",'wb'))