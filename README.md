*************************************************************************
Readme.txt for sentistock (version 1.2)
http://www.stock-websense.rhcloud.com/readme.txt
*************************************************************************


       #####                            #####                             
      #     # ###### #    # ##### #    #     # #####  ####   ####  #    # 
      #       #      ##   #   #   #    #         #   #    # #    # #   #  
       #####  #####  # #  #   #   #     #####    #   #    # #      ####   
            # #      #  # #   #   #          #   #   #    # #      #  #   
      #     # #      #   ##   #   #    #     #   #   #    # #    # #   #  
       #####  ###### #    #   #   #     #####    #    ####   ####  #    # 



Name	:SentiStock

Version	:1.2

Authors:
* Anenth Vishnu K.P. (anenth.us at gmail.com)
* Jovin George (jjovin2010 at gmail.com)
* Mevin Babu Chirayath (mevinbabuc at gmail.com)
* Rohit Vincent (therohitvincent at gmail.com)

Date	:April 26,2013

I.	Description
	
	SentiStock is an open-source sentiment analysis program , which 
	analyzes social networking sites for optimal stock market 
	investments.

	SentiStock is a python program which process tweets from twitter 
	as input and classifies them using a Bayesian classifier.This 
	helps us in identifying the potential stock.
	SentiStock does linear regression on stock values to predict the 
	future stock values, thus enabling the user to find out how much 
	he should invest in.
	
	SentiStock runs on Linux - redhat's cloud server(OpenShift)

II.	Required systems.

	Python 2.6/2.7	- Python language interpretter
	MySQL 5.1	- MySQL database server
	Cron		- Linux Scheduler

III.	Packages Required
	
	NLTK		- Natural Language Tool Kit
	tweetstream	- Python wrapper for twitter API
	Web.py		- web.py is a web framework for Python
	pytz		- Accurate calculations using Python
	anyjson		- JSON wrapper for python libraries
	Jinja2		- Template engine for the Python
	
IV.	Installation

	SentiStock has been designed to run on Openshift Cloud server.
	To run it locally you have to install Openshift locally and deploy
	SentiStock in it.
	
	Instructions to install Openshift Cloud server can be found here:
	https://www.openshift.com/wiki/build-your-own-paas-from-the-openshift-origin-livecd-using-liveinst
	
	To install on a virtual system follow this link :
	https://www.openshift.com/wiki/getting-started-with-openshift-origin-livecd-and-virtmanager

	After the installation of the Server the cartridges required to run the apps are : 
	
		Python 2.6
		MySQL 5.1
		Cron 1.4

	The app to deploy can be found in the SentiStock/ folder.
	The database to get started can be found in SentiStock/db/ folder.

	To run individual modules of the app you can run it directly by 
	executing : python filename.py

V.	Compatibiltiy

	This tool requires Python 2.6/2.7 and latest MySQL server.
	This tool is tested only on Redhat,but should work on other Linux 
	platforms as well.
	SentiStock is not compatible with python 3.x .To make it work in 
	Python 3.x , you can try using gevent as your python webserver.


VI.	Contacts

	For queries on deploying the application,cron scheduling and NLP
		Mevin Babu Chirayath (mevinbabuc at gmail.com)
	
	For queries on front end, charts and web.py
		Anenth Vishnu (anenth.us at gmail.com)

	For queries on Database management and Data Collection
		Rohit Vincent (therohitvincent at gmail.com)

	For queries on Sentiment analysis and Linear Regression
		Jovin George (jjovin2010 at gmail.com)
	
	For Bug fixes,making request and submit patches
		Mevin Babu Chirayath (mevinbabuc at gmail.com)

VII.	Code.

	Get the latest code from Github 
	https://github.com/mevinbabuc/senti-stock

VIII.	Copyrights and Licence


	Copyright [2013] [Mevin Babu]

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
