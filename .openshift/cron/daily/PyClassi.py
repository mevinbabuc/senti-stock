#! /usr/bin/python

from math import log,exp
from re import sub,compile
from collections import defaultdict
import cPickle as pickle,MySQLdb,gc,PyNegator as neg#,SpellCheck as sp
from nltk import stem

direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/bigdata/"
out_dir="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/data/"

#close unnecessary connections
gc.collect()

# tweet_filter=compile(r"[\\]|[()]|[)]|[\"]|[']|[,]|[!]|[.]|[#][^ ]+|[&]|[-]|[?]|[_]|((http|https)://)[^ ]+|\w*[@][^ ]+|\b[\S0-9]\b|\b[0-9]+\b")
tweet_filter=compile(r"[\\]|[()]|[)]|[\"]|[']|[,]|[!]|[.]|[#][^ ]+|[$][^ ]+|[&]|[-]|[?]|[_]|((http|https)://)[^ ]+|\w*[@][^ ]+|\b[\S0-9]\b|\b[0-9]+\b")
word_normalize=compile(r'(\w)\1+') #remove repeating charecters

dicSpell=pickle.load(open(direct+"spell.blu",'rb')) #load spell check words
dicSyn=pickle.load(open(direct+"synonym.blu",'rb')) #load synonym words
stop=pickle.load(open(direct+"stopwords.blu",'rb')) #load stop words
#load superstopwords
# dicStop=pickle.load(open("superstopwords.blu",'rb')) 


aapl_posd=pickle.load(open(out_dir+'aapl_Unipositive.p','rb'))
aapl_pos_dic_len=len(aapl_posd)

aapl_negd=pickle.load(open(out_dir+'aapl_Uninegative.p','rb'))
aapl_neg_dic_len=len(aapl_negd)

bac_posd=pickle.load(open(out_dir+'bac_Unipositive.p','rb'))
bac_pos_dic_len=len(bac_posd)

bac_negd=pickle.load(open(out_dir+'bac_Uninegative.p','rb'))
aapl_neg_dic_len=len(bac_negd)

goog_posd=pickle.load(open(out_dir+'goog_Unipositive.p','rb'))
goog_pos_dic_len=len(goog_posd)

goog_negd=pickle.load(open(out_dir+'goog_Uninegative.p','rb'))
goog_neg_dic_len=len(goog_negd)


# total_len=float(pos_dic_len+neg_dic_len)

def classify(line,Company):
    log_sum_pos=0.0
    log_sum_neg=0.0
    log_deno=0.0

    if Company=="aapl" :
        posd=aapl_posd
        negd=aapl_negd
    elif Company=="bac" :
        posd=bac_posd
        negd=bac_negd
    elif Company=="goog" :
        posd=goog_posd
        negd=goog_negd

    lne=""
    tweet=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line.lower()))).split() #twitter hack!                                              
    for feature in tweet:
        #print feature
        #word=feature
        if dicSpell.has_key(feature):
            feature=dicSpell[feature]
        #feature=sp.correct(feature)
        word=stem.PorterStemmer().stem(feature)
        if word not in stop:
            if dicSyn.has_key(word):
                word=dicSyn[word]
        lne=lne+" "+word
    lne = neg.replace_negations(lne)
 
    # bi=defaultdict(int)

    feature=set(list(lne.split()))
    # for word in range(0,len(feature)-1):
    #     bi[feature[word]+" "+feature[word+1]]+=1
        
    for word in feature:
        temp=0.0
        if word in posd:
            temp=float(posd[word])
            log_sum_pos+=log(float(temp))#/(pos_dic_len/total_len))
            #print "Positive",word,log_sum_pos,posd[word],temp
        if word in negd:
            temp+=float(negd[word])
            log_sum_neg+=log(float(temp))
            #print "\nNegative",word,log_sum_pos,negd[word],temp
        if temp>0 :
            log_deno+=log(temp)
            log_sum_pos+=log(2.1)
            log_sum_neg+=log(1)
            #print "\nTemp > 0",word,temp,log_sum_pos

    #print "VALUES",log_deno,log_sum_pos

    log_pos_prob=log(0.5)
    log_neg_prob=log(0.5)

    #log_sum=log_sum_pos+log_sum_neg+log_pos_prob

    log_sum=(log_sum_pos+log_pos_prob)-log_deno
    n_log_sum=(log_sum_neg+log_neg_prob)-log_deno

    difference=exp(log_sum)-exp(n_log_sum)

    print Company,difference,line
    #print log_sum,line
    if difference>=0.1:
        return 2
    else:
        return 0 #BAD NEGATIVE