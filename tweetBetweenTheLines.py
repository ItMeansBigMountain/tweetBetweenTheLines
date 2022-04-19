'''
Scores are rated as followed:

    Polarity (how negative or positive a statment is):
        1 = Positive
        -1 = Negative

    Subjectivity (how much of an opinion something is):
        1 = Opinionated
        0 = Stated as fact


'''




import tweepy 
import pprint
from textblob import TextBlob
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

# GLOBAL VARIABLES
consumer_key = "" 
consumer_secret = ""
access_key = ""
access_secret = ""





def get_all_tweets():
    #RATINGS LIST ON LINE 90
    screen_name = input('Type in Twitter handle you would like it look up: ')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id
    while len(new_tweets) > 0:
        print ("getting tweets before tweet.id: %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    
    outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]
    return outtweets

# functional functions
def graphing(scores):
    labels = [
        "Sentence" ,
        "Word"
    ]

    print(scores['Polarity'])
    print(scores['Subjectivity'] )
    # exit()


    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2 , scores['Polarity'] , width, label='Polarity')
    rects2 = ax.bar(x + width/2 , scores['Subjectivity'] , width, label='Subjectivity')

    # Add some text for labels, Subjectivity and custom x-axis tick labels, etc.
    ax.set_ylabel('Polarity / Intensity')
    ax.set_title('Tweet Sentiment')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()


def main():
    all_tweets = get_all_tweets()
    
    sentimentArrSENTENCE = []
    sentimentArrWORD = []

    sentencePolarity = 0
    sentenceSubjectivity = 0
    
    countSentence = 0
    countWord = 0

    for tweet in all_tweets:
        for x in tweet:

            quote = str(x)[1:]
            wiki = TextBlob(str(quote))

            # SENTENCE sentiment
            value = (wiki.sentiment.polarity , wiki.sentiment.subjectivity)
            sentencePolarity += value[0]
            sentenceSubjectivity += value[1]
            sentimentArrSENTENCE.append(value)




            # WORD in sentence sentiment+
            words = wiki.words
            
            
            print(words)
            print()


            eachWordValue = [(TextBlob(y).sentiment.polarity , TextBlob(y).sentiment.subjectivity) for y in words ]
            sentimentArrWORD.extend(eachWordValue)
    wordPolarity = 0 #adding word sentiments
    wordSubjectivity = 0
    for x in sentimentArrWORD:
        wordPolarity += x[0]
        wordSubjectivity += x[1]






    # SENTENCE AVERAGE 
    averageSentence_Polarity = ( sentencePolarity /  len(sentimentArrSENTENCE) )
    averageSentence_Subjectivity = ( sentenceSubjectivity / len(sentimentArrSENTENCE)  )



    # WORDS AVERAGE 
    averageWord_Polarity = ( wordPolarity /  len(sentimentArrWORD) )
    averageWord_Subjectivity = ( wordSubjectivity /  len(sentimentArrWORD)  )




    print(f'\n\nTotals for sentences\nPolarity: {sentencePolarity}\nSubjetivity: {sentenceSubjectivity}\n\nAVERAGE out of {len(sentimentArrSENTENCE)}\nPolarity: {averageSentence_Polarity}\nSubjectivity: {averageSentence_Subjectivity}')

    print('------------------')
    
    print(f'\n\nTotals for all words used\nPolarity: {wordPolarity}\nSubjetivity: {wordSubjectivity}\n\nAVERAGE out of {len(sentimentArrWORD)}\nPolarity: {averageWord_Polarity}\nSubjectivity: {averageWord_Subjectivity}')


    # GRAPH
    scores = {
        'Polarity' : [ averageSentence_Polarity , averageWord_Polarity  ],
        'Subjectivity' : [ averageSentence_Subjectivity , averageWord_Subjectivity    ]
    }
    graph = graphing(scores)






main()