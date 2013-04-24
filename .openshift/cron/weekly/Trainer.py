#! /usr/bin/python

from re import sub,compile
from nltk import stem
from Queue import Queue
import limits,MySQLdb,threading,gc,csv,cPickle as pickle,PyNegator as neg#,SpellCheck as sp
from collections import defaultdict

direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/bigdata/"
out_dir="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/data/"

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
aapl_pos_workq=Queue()
bac_pos_workq=Queue()
goog_pos_workq=Queue()
aapl_neg_workq=Queue()
bac_neg_workq=Queue()
goog_neg_workq=Queue()

def make_Queue(filename):
    config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'backup'}
    cnx = MySQLdb.connect(**config)
    
    neg_cur=cnx.cursor()
    pos_cur=cnx.cursor()
    get_neg_tweet = "select * from tweets_"+filename+" where sentiment=0 "
    get_pos_tweet = "select * from tweets_"+filename+" where sentiment=2 "
    
    neg_cur.execute(get_neg_tweet)
    pos_cur.execute(get_pos_tweet)
    
    db_neg_tweets = neg_cur.fetchall()
    db_pos_tweets = pos_cur.fetchall()
    
    if filename=="aapl":
        for line in db_neg_tweets:
            lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
            # print lne
            aapl_neg_workq.put(lne)
        for line in db_pos_tweets:
            lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
            # print lne
            aapl_pos_workq.put(lne)
    elif filename=="goog":
        for line in db_neg_tweets:
            lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
            # print lne
            goog_neg_workq.put(lne)
        for line in db_pos_tweets:
            lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
            # print lne
            goog_pos_workq.put(lne)
    elif filename=="bac":
        for line in db_neg_tweets:
            lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
            # print lne
            bac_neg_workq.put(lne)
        for line in db_pos_tweets:
            lne=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line[1].lower())))
            # print lne
            bac_pos_workq.put(lne)
        
    cnx.close()

#extract bi-gram features and places them in Queues for word counting
aapl_pos_processq=Queue()
bac_pos_processq=Queue()
goog_pos_processq=Queue()
aapl_neg_processq=Queue()
bac_neg_processq=Queue()
goog_neg_processq=Queue()

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
            for word in range(0,len(feature)):
                unigram=self.filter(feature[word])

                # Antonym replacer
                # bigram=neg.replace_negations(bigram)

                self.processq.put(unigram)
            self.workq.task_done()



aapl_pos_Unigramdic=defaultdict(int)
goog_pos_Unigramdic=defaultdict(int)
bac_pos_Unigramdic=defaultdict(int)
aapl_neg_Unigramdic=defaultdict(int)
goog_neg_Unigramdic=defaultdict(int)
bac_neg_Unigramdic=defaultdict(int)

lock=threading.RLock()

#count the word frequency
class ThreadFreq(threading.Thread):
    
    def __init__(self,processq,id,Unigramdic):
        threading.Thread.__init__(self)
        self.processq=processq
        self.Unigramdic=Unigramdic
        self.id=id
    
    def run(self):
        while True:
            unigram=self.processq.get()
            with lock:
                if unigram.strip()!='' :
                    self.Unigramdic[unigram.strip()]+=1
                    # print unigram.strip()
            #print self.processq.qsize()
            self.processq.task_done()


#Thread Generation !

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(aapl_pos_workq,aapl_pos_processq,i)
    t.setDaemon(True)
    t.start()

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(aapl_neg_workq,aapl_neg_processq,i)
    t.setDaemon(True)
    t.start()

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(goog_pos_workq,goog_pos_processq,i)
    t.setDaemon(True)
    t.start()

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(goog_neg_workq,goog_neg_processq,i)
    t.setDaemon(True)
    t.start()

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(bac_pos_workq,bac_pos_processq,i)
    t.setDaemon(True)
    t.start()

for i in range(limits.ExtractThreadLimit):
    t=ThreadExtract(bac_neg_workq,bac_neg_processq,i)
    t.setDaemon(True)
    t.start()

print "started filling the queue"
make_Queue("aapl")
make_Queue("bac")
make_Queue("goog")
print "Queue full"

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(aapl_pos_processq,i,aapl_pos_Unigramdic)
    tf.setDaemon(True)
    tf.start()

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(aapl_neg_processq,i,aapl_neg_Unigramdic)
    tf.setDaemon(True)
    tf.start()

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(goog_pos_processq,i,goog_pos_Unigramdic)
    tf.setDaemon(True)
    tf.start()

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(goog_neg_processq,i,goog_neg_Unigramdic)
    tf.setDaemon(True)
    tf.start()

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(bac_pos_processq,i,bac_pos_Unigramdic)
    tf.setDaemon(True)
    tf.start()

for i in range(limits.FrequencyThreadLimit):
    tf=ThreadFreq(bac_neg_processq,i,bac_neg_Unigramdic)
    tf.setDaemon(True)
    tf.start()


#Waiting for the Threads!


aapl_pos_processq.join()
aapl_neg_processq.join()
goog_pos_processq.join()
goog_neg_processq.join()
bac_pos_processq.join()
bac_neg_processq.join()

# Frequency Filtering

aapl_negunidic=defaultdict(int)
bac_posunidic=defaultdict(int)
goog_posunidic=defaultdict(int)
aapl_posunidic=defaultdict(int)
bac_negunidic=defaultdict(int)
goog_negunidic=defaultdict(int)




for word in aapl_pos_Unigramdic:
    tmp=aapl_pos_Unigramdic[word]
    print tmp
    if tmp > limits.UNI_Threshold:
        aapl_posunidic[word]=tmp

with open(direct+'pos_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in aapl_posunidic:
            aapl_posunidic[row[0]]+=(float)(row[1])   
            #print row[0]     

pickle.dump(aapl_posunidic,open(out_dir+"aapl_Unipositive.p",'wb'))

for word in aapl_neg_Unigramdic:
    tmp=aapl_neg_Unigramdic[word]
    if tmp > limits.UNI_Threshold:
        aapl_negunidic[word]=tmp

with open(direct+'neg_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in aapl_negunidic:
            aapl_negunidic[row[0]]+=(float)(row[1])   
            #print row[0]     

pickle.dump(aapl_negunidic,open(out_dir+"aapl_Uninegative.p",'wb'))




for word in bac_pos_Unigramdic:
    tmp=bac_pos_Unigramdic[word]
    if tmp > limits.UNI_Threshold:
        bac_posunidic[word]=tmp

with open(direct+'pos_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in bac_posunidic:
            bac_posunidic[row[0]]+=(float)(row[1])   
            #print row[0]     

pickle.dump(bac_posunidic,open(out_dir+"bac_Unipositive.p",'wb'))

for word in bac_neg_Unigramdic:
    tmp=bac_neg_Unigramdic[word]
    if tmp > limits.UNI_Threshold:
        bac_negunidic[word]=tmp

with open(direct+'neg_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in bac_negunidic:
            bac_negunidic[row[0]]+=(float)(row[1])   
            #print row[0]     

pickle.dump(bac_negunidic,open(out_dir+"bac_Uninegative.p",'wb'))


for word in goog_pos_Unigramdic:
    tmp=goog_pos_Unigramdic[word]
    if tmp > limits.UNI_Threshold:
        goog_posunidic[word]=tmp

with open(direct+'pos_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in goog_posunidic:
            goog_posunidic[row[0]]+=(float)(row[1])   
            #print row[0]     

pickle.dump(goog_posunidic,open(out_dir+"goog_Unipositive.p",'wb'))

for word in goog_neg_Unigramdic:
    tmp=goog_neg_Unigramdic[word]
    print goog_neg_Unigramdic[word]
    if tmp > limits.UNI_Threshold:
        goog_negunidic[word]=tmp

with open(direct+'neg_bag.txt','rb') as bag_data:
    sr=csv.reader(bag_data,delimiter=' ')
    for row in sr:
       # print row[0]
       if row[0] in goog_negunidic:
            goog_negunidic[row[0]]+=(float)(row[1])   
            #print row[0]     


pickle.dump(goog_negunidic,open(out_dir+"goog_Uninegative.p",'wb'))
