import MySQLdb

config = {'user': 'adminzQa3Yqe','passwd': 'RDKC1VlNyLSg','host': '127.7.115.1','db': 'sentistock'}
cnx = MySQLdb.connect(**config)

cur=cnx.cursor()
get_neg_tweet = "select * from tweets_aapl where sentiment=1 union select * from tweets_bac where sentiment=1 union select * from tweets_goog where sentiment=1"
cur.execute(get_neg_tweet)

db_tweets = cur.fetchall()

for line in db_tweets:
	print line[1].lower()