import tweepy 
import pprint

import matplotlib.pyplot as plt


# GLOBAL VARIABLES
consumer_key = "" 
consumer_secret = ""
access_key = ""
access_secret = ""


screen_name = input('Type in Twitter handle you would like it look up: ')
list_of_words = []
for x in range(1,5):
	searchWord = input(str(x)+': Please enter the word you want to search users tweets with: ')
	list_of_words.append(searchWord)



def opening():
	print( '\nA doing of Oyama Productions' , '\n')
	print('Looking Up:','@'+screen_name)
	print('Looking for:', list_of_words)
	pass

def get_all_tweets(screen_name):

	#RATINGS LIST ON LINE 90

	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before tweet.id: %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1 #since you cant grab all of them, you must lower the "last id"

		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]

	totals_list = [] #each search word has a total found appended to this list
	found_total = 0 #all found count
	didntFind_count = 0

	for word in list_of_words:
		word = str(word)
		print('\n',word)
		print('===========================')
		found_count = 0

		for x in outtweets:
			string = str(x)
			if  (string.find(str(word)) != -1): #if search word does not equal None!
				found_count += 1 #---- found count of each search word
				found_total += 1
				pprint.pprint(string) 
			else:
				didntFind_count += 1

		totals_list.append(found_count)



	#this is where things intresting
	# rating_list = [SCORES OF EACH WORD IN list_of_words GOES HERE (cronilogical order)]
	rating_list = [5,10,15,20]
	score_list = []
	for x in range(0,len(totals_list)):
		score_list.append(rating_list[x] * totals_list[x])

	print('Totals list')
	print(totals_list)
	print('scores list')
	print(score_list)

	print("\nDidnt find words in", str(didntFind_count),"tweets")
	
	
	for x in range(len(totals_list)):
		print(list_of_words[x])
		print(totals_list[x])
		print('--------------------------\n')


	# return score_list if you want charts to show ratings****
	return totals_list


def graphing(scores):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = list_of_words
	sizes = scores
	explode = (0, 0, 0, 0) 
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
			shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	plt.show()




# FUNCTIONS TO CALL 
opening()
scores = get_all_tweets(screen_name)
graph = graphing(scores)

