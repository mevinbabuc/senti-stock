
import cPickle as pickle
from collections import defaultdict

direct="/var/lib/openshift/512e12ac4382ec1abb000384/app-root/runtime/repo/data/bigdata/"

dic=pickle.load(open(direct+"antonym.blu",'rb'))


def replace(word):
	if word in dic:
		return dic[word]
	else:
		return "not "+word

def replace_negations(senten):
	sent=senten.split()
	i, l = 0, len(sent)
	words = ""
	while i < l:
		word = sent[i]
		if word == "not" and i+1 < l:
			ant = replace(sent[i+1])
			if ant:
				words=words+" "+ant
				i += 2
				continue
		words=words+" "+word
		i += 1
	return words.strip()