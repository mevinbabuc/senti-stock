#! /usr/bin/python

import PyClassi as Classifier
from re import sub
import PyNegator

test=open("test.txt")
correct=0
wrong=0
falsepositive=0
falsenegative=0

for line in test.readlines():
	status=line[0]
	lne=sub(r"[!]|[.]|[#][^ ]+|[&]|[-]|[?]|[_]|((http|https)://)[^ ]+|\w*[@][^ ]+|\b[\S0-9]\b",'',line.lower())
	classi=Classifier.classify(lne)

	if status=='0': #polarity representation reversed for database representation sake :-/
		if classi==status:
			correct+=1
		else:
			falsepositive+=1
			wrong+=1
	elif status=='1':
		if classi==status:
			correct+=1
		else:
			falsenegative+=1
			wrong+=1
	print "Correct : ",correct,"\n Wrong : ",wrong,"\n falsenegative : ",falsenegative,"\n falsepositive",falsepositive
	print "\n ratio : ",(float(correct)/(correct+wrong))*100