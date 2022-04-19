import tweepy 
import pprint


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
final_word_dict = {}

def opening():
	print( '\nA doing of Oyama Productions' , '\n')
	print('Looking Up:','@'+screen_name)
	print('Looking for:', list_of_words)
	pass

def get_all_tweets(screen_name):

	#Twitter only allows access to a users most recent 3240 tweets with this method
	
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
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before tweet.id: %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
	found_total = 0

	for word in list_of_words:
		word = str(word)
		print('\n',word)
		print('===========================')
		found_count = 0
		didntFind_count = 0

		for x in outtweets:
			string = str(x)
			if  (string.find(str(word)) != -1):
				found_count += 1
				found_total += 1
				final_word_dict.update({str(word) +"~"+ str(found_count) : str(string)}) 
				pprint.pprint(string) 

			else:
				didntFind_count += 1
				
	pprint.pprint(final_word_dict)
	print("\nDidnt find these words in", str(didntFind_count),"tweets")
	print("\nWe found", str(found_total),"tweets")

# FUNCTIONS TO CALL 
opening()
get_all_tweets(screen_name)

