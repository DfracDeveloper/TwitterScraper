import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
# from dashboard import *

# @st.cache
def scrape_data(keyword, limit, filename):
    path = 'data/'
    query_string = keyword
    tweets_list = []
    limits = int(limit)
    df = pd.DataFrame()

    for tweet in sntwitter.TwitterSearchScraper(query_string).get_items():
        if len(tweets_list) == limits:
            break
        else:
            # appending data to tweets list
            tweets_list.append([tweet.id, tweet.conversationId, tweet.date, tweet.lang, tweet.content, tweet.user.username, tweet.user.id, tweet.user.displayname, 
            tweet.user.description, tweet.user.created, tweet.user.verified, tweet.user.followersCount, tweet.user.friendsCount, tweet.user.location, tweet.hashtags, tweet.mentionedUsers,
            tweet.quotedTweet, tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.quoteCount, tweet.inReplyToTweetId, tweet.inReplyToUser, tweet.retweetedTweet, 
            tweet.outlinks, tweet.place, tweet.coordinates, tweet.url])

    # Creating a dataframe with the tweets list
    tweets_df = pd.DataFrame(tweets_list, columns=["Tweet Id", "Conversation Id", "Date", "Language", "Content", "Username", "User Id", "User Display Name", 
    "User Description", "User Created", "User Verified", "User Followers", "User Following", "User Location", "Hashtags", "Users Mentioned",
    "Quoted Tweet", "Total Likes", "Total Replies", "Total Retweets", "Total Quotes", "Reply to Tweet Id", "Reply to User", "Retweeted Tweet", "Outlinks", "place",
    "Coordinates", "Tweet Url"])

    # tweets_df.to_csv(path + filename + '.csv', encoding="UTF-8", index=False)

    return tweets_df