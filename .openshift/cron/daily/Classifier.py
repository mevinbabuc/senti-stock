#! /usr/bin/python

from math import log,exp
from re import sub,compile
from collections import defaultdict
import limits,cPickle as pickle,PyNegator as neg#,SpellCheck as sp
from nltk import stem

tweet_filter=compile(r"[\\]|[()]|[)]|[\"]|[']|[,]|[!]|[.]|[#][^ ]+|[&]|[-]|[?]|[_]|((http|https)://)[^ ]+|\w*[@][^ ]+|\b[\S0-9]\b|\b[0-9]+\b")
word_normalize=compile(r'(\w)\1+') #remove repeating charecters

dicSpell=pickle.load(open("spell.blu",'rb')) #load spell check words
dicSyn=pickle.load(open("synonym.blu",'rb')) #load synonym words
stop=pickle.load(open("stopwords.blu",'rb')) #load stop words



posunigramdic=pickle.load(open('Unipositive.p','rb'))
posBigramdic=pickle.load(open('Bipositive.p','rb'))

pos_dic_len=len(posunigramdic)+len(posBigramdic)

# print "Positive Dictionsary"
# print posd

negunigramdic=pickle.load(open('Uninegative.p','rb'))
negBigramdic=pickle.load(open('Binegative.p','rb'))

neg_dic_len=len(negunigramdic)+len(negBigramdic)

# print "Negative Dictionary"
# print negd

total_len=float(pos_dic_len+neg_dic_len)

def filter_tweet(word):

    # Spell check
    if dicSpell.has_key(word):
                word=dicSpell[word]
    # Stem the words
    WordStem=stem.PorterStemmer().stem(word)

    if WordStem in stop:
        WordStem=""
    else :
        # Synonym replacement
        if dicSyn.has_key(WordStem):
            WordStem=dicSyn[WordStem]

    return WordStem


def classify(line):
    log_sum_pos=0.0
    log_deno=0.0
    # line=raw_input()

    tuple=tweet_filter.sub("",word_normalize.sub(r'\1\1',sub(r'(\w)\1+\b', r'\1', line.lower())))

    #Convert tweet into a list of words
    feature=list(tuple.split())

    for word in range(0,len(feature)-1):
        bigram=filter_tweet(feature[word])+" "+filter_tweet(feature[word+1])

        # Antonym replacer
        bigram=neg.replace_negations(bigram)

        temp=0.0
        if len(bigram) > 1:

            unigramList=bigram.split()
            if bigram in posBigramdic:
                temp=float(posBigramdic[bigram])
                log_sum_pos+=log(float(temp)/(pos_dic_len/total_len))
                if temp>0 :
                    log_deno+=log(temp)

            else :

                for unigram in unigramList:
                    if unigram in posunigramdic:
                        temp=float(posunigramdic[unigram])
                        log_sum_pos+=log(float(temp)/(pos_dic_len/total_len))
                        if temp>0 :
                            log_deno+=log(temp)


            if bigram in negBigramdic:
                temp+=float(negBigramdic[bigram])
                if temp>0 :
                    log_deno+=log(temp)

            else :
                for unigram in unigramList:
                    if unigram in negunigramdic:
                        temp=float(negunigramdic[unigram])
                        if temp>0 :
                            log_deno+=log(temp)

        else :
            if bigram in posunigramdic:

                temp=float(posunigramdic[bigram])
                log_sum_pos+=log(float(temp)/(pos_dic_len/total_len))

            if bigram in negunigramdic:
                temp+=float(negunigramdic[bigram])

            if temp>0 :
                log_deno+=log(temp)



            #print "\nTemp > 0",word,temp,log_sum_pos

    #print "VALUES",log_deno,log_sum_pos

    log_pos_prob=log(0.5)

    #log_sum=log_sum_pos+log_sum_neg+log_pos_prob

    log_sum=(log_sum_pos+log_pos_prob)-log_deno

    print exp(log_sum),line
    #print log_sum,line
    if exp(log_sum)>limits.ClassifierThreshold:
        return '1'
    else:
        return '0'