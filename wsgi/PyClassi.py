from math import log,exp
from re import sub,compile
import cPickle as pickle
from nltk import stem


direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/"

# search for keywords from input in the positive dictionary

#data=open("data.txt")
#line=data.readline().lower()


def classify(line):
    tweet_filter=compile(r'(@[A-Za-z0-9]+)|(\w+:\/\/\S+)|(#[^ ]+)')
    word_normalize=compile(r'(\w)\1+') #remove repeating charecters

    # read the positive features into a dictinary
    posd=pickle.load(open(direct+'posdic.p','rb'))
    pos_dic_len=len(posd)
    log_sum_pos=0.0


    # read the negative features into a dictinary
    negd=pickle.load(open(direct+'negdic.p','rb'))
    neg_dic_len=len(negd)
    log_sum_neg=0.0 # not used !
    log_deno=0.0
    total_len=float(pos_dic_len+neg_dic_len)

    tweet=set(tweet_filter.sub("",word_normalize.sub(r'\1\1',line.lower())).split())  #twitter hack!                                              
    for feature in tweet:
        #word=feature
        word=stem.PorterStemmer().stem(feature)
        temp=0.0
        if word in posd:
            temp=float(posd[word])
            log_sum_pos+=log(float(temp)/(pos_dic_len/total_len))
            #print "Positive",word,log_sum_pos,posd[word],temp
        if word in negd:
            temp+=float(negd[word])
            #print "\nNegative",word,log_sum_pos,negd[word],temp
        if temp>0 :
            log_deno+=log(temp)
            #print "\nTemp > 0",word,temp,log_sum_pos

    #print "VALUES",log_deno,log_sum_pos

    log_pos_prob=log(0.5)

    #log_sum=log_sum_pos+log_sum_neg+log_pos_prob

    log_sum=(log_sum_pos+log_pos_prob)-log_deno

    return exp(log_sum)