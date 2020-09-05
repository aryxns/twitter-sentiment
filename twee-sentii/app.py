import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit as st
import pandas as pd

auth = tweepy.OAuthHandler("PfXYT2xpRcdCURbMk7qPbLeZb", "ujTSVB9Ljr3XOQmlvoLfu5L4LNu4AX8gG9hZlan9QF0stkciOU")
auth.set_access_token("1125757371861520389-Z4EJSd0NNdXRo6dbazq9CMYKm2s0Q1", "4Lej5ggKfVQlc5h0KEGr50tm4eAaa80fmCLPP2ZELpEwn")

api = tweepy.API(auth)

analyser = SentimentIntensityAnalyzer()
class StreamListener (tweepy.StreamListener):
	def on_status(self, status):
		if not stop1:
			text= status.text
			score = analyser.polarity_scores(text)
			st.write(text)
			st.write("----------------------------------------------------------------------------------")
			df = pd.DataFrame([score])
			df = df.drop("compound", axis=1)
			pos = df['pos'].item()
			neg = df['neg'].item()
			neu = df['neu'].item()
			if pos > neu and neg:
				answer = str(pos * 100)
				st.write("Analyzed as Positive by " + answer + "%")
			elif neg > neu or pos:
				answer = str(neg * 100)
				st.write("Analyzed as Negative by " + answer + "%" )
			elif neu > neg and pos:
				answer = str(neu * 100)
				st.write("Analyzed as Neutral by " + answer + "%")
			st.write("----------------------------------------------------------------------------------")
			#st.write("The sentiment is: {}".format(str(score
			return True
		else:
			exit()
			return False

def stream_tweets(tag):
	listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True, wait_on_rate_limit_notify=True))
	streamer = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')
	query = [str(tag)]
	streamer.filter(track=query, languages=['en'])

st.header("Tweet sentiment analysis")
st.write('Enter a hashtag and a stream of latest tweets containing the hastag will start below. The sentiment will be listed below the stream.')
st.write("----------------------------------------------------------------------------------")
t = st.text_input("Enter a hashtag to start stream of tweets")

start1 = st.button('Get tweets')

stop1 = st.button('reset')
st.write("----------------------------------------------------------------------------------")

if start1:
	stream_tweets(str(t))