import tweepy 
import pprint


# GLOBAL VARIABLES
consumer_key = "" 
consumer_secret = ""
access_key = ""
access_secret = ""


# USER INPUT search words
screen_name = input('Type in Twitter handle you would like it look up: ')



def opening():
	print( '\nA doing of Oyama Productions' , '\n')
	print('Looking Up:','@'+screen_name)
	pass

def get_all_tweets(screen_name):

	# //////////// FETCH TWEETS
	# AUTH tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	# INIT populate alltweets with first set
	alltweets = []	
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1
	# APPEND sets of historical data
	while len(new_tweets) > 0:
		# ITERATIVE PUSH
		print ("getting tweets before tweet.id: %s" % (oldest))
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	outtweets = [tweet_text.text for tweet_text in alltweets]




	# //////////// SEARCH WITHIN TWEETS
	while True:
		# ask user for new search words
		list_of_words = []
		final_word_dict = {}
		for x in range(1,5):
			searchWord = input(str(x)+': Please enter the word you want to search users tweets with: ')
			list_of_words.append(searchWord)


		# SEARCH for input words 
		found_total = 0
		for word in list_of_words:
			found_count = 0
			didntFind_count = 0
			for x in outtweets:
				string = str(x)
				if  (string.find(str(word)) != -1):
					found_count += 1
					found_total += 1
					if word in final_word_dict:
						final_word_dict[word].append(  str(string)  )
					else:
						final_word_dict[word] = [ str(string) ]
				else:
					didntFind_count += 1
					

		# OUTPUT
		pprint.pprint(final_word_dict)
		print("\nDidnt find these words in", str(didntFind_count),"tweets")
		print("\nWe found", str(found_total),"tweets")


		# end program 
		end = input("would you like to search again? (y/n) :  ").lower().startswith("n")
		if end: exit()




# FUNCTIONS TO CALL 
opening()
get_all_tweets(screen_name)

