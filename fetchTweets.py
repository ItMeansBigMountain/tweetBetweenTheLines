import tweepy 
from pprint import pprint
import json



# AUTH
def authentificationTW():
	# GLOBAL VARIABLES
	consumer_key = "" 
	consumer_secret = ""
	access_key = ""
	access_secret = ""


	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	return api

def get_all_tweets( api ,screen_name):
	
	#initialize a list to hold all the tweepy Status() Objects
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
	
	# list of strings 
	outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
	return outtweets

def analyze_Tweets(api , screen_name):

	# FETCHING TWEETS  (seems to only grab 3k tweets)
	tweets = []
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	tweets.extend(new_tweets)
	oldest = tweets[-1].id - 1
	while len(new_tweets) > 0:
		print ("getting tweets before tweet.id: %s" % (oldest))
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		tweets.extend(new_tweets)
		oldest = tweets[-1].id - 1
		print ("...%s tweets downloaded so far" % (len(tweets)))


	# SORTING TWEETS
	for x in tweets:
		json_str = json.dumps(x._json) #converting
		json_Dict = json.loads(json_str)

		# dict_keys(['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang']

		# TODO
		# find buzz words
		# what timeframe this popularity is
		# add to an array then make it a set at the end of the loop


		print(   f"{json_Dict['text'] = }"   )
		print(   f"{json_Dict['geo'] = }"   )
		print(   f"{json_Dict['coordinates'] = }"   )
		print(   f"{json_Dict['retweet_count'] = }"   )
		print(   f"{json_Dict['favorite_count'] = }"   )
		print(   f"{json_Dict['created_at'] = }"   )
		print()


		# social Exposure per tweet
		retweets = json_Dict['retweet_count']
		fav = json_Dict['favorite_count']
		Social_Exposure = retweets + fav



		# DEBUG EXPERIMENTAL
		# go through them again and check the total
		for y in range( 0 ,  len(tweets)  , 1  ):
			json_str = json.dumps(tweets[y]._json) 
			json_Dict = json.loads(json_str)
			compare_Exposure =  json_Dict['retweet_count'] + json_Dict['favorite_count']
			

	print( "ANALYZING" ,  len(tweets) , "TWEETS")
	print("analysis code not complete... please read comments within this function.")








# calling functions down here

# AUTH
api = authentificationTW()

# INTERNAL FETCH TWEETS
# string_arr_tweets = get_all_tweets(api , 'wallstreetbets')

# ANALYSIS
analyze_Tweets(api, 'elonmusk' )

