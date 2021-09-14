# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:11:15 2019

@author: Emmanuel
"""
#import external pandas_datareader library with alias of web
from yahoo_fin import stock_info as si;
import pandas_datareader as web;
import matplotlib.pyplot as plt;
import pandas as pd;
#import plotly.express as px
import datetime;
import csv;
import re;
#sentiment analysis dependencies
import tweepy;
from textblob import TextBlob as tb;
#twitter keys
api_key = "S88HUSqaE9tubL7Ly6xLidI7s";
api_secret_key = "fxYiwUnsxMyfiyxgHjtGNQBPwHuv6RGmfbQ6ScW6XR6111JPRt";

access_token = "914994120501972992-4ZGLy02zsONjvk9iQ27lEr0W751cHpM";
access_secret_token = "yFH7krYa4XvjY79MMLIpc0iAMcm46Jyib5h43mBedAHjw";
#login
auth = tweepy.OAuthHandler(api_key, api_secret_key);
auth.set_access_token(access_token, access_secret_token);
api = tweepy.API(auth);

def getTweets(ticker):
    public_tweets = [status for status in tweepy.Cursor(api.search, q=ticker).items(100)];
    return public_tweets;

def analyzeTweets(tweets):
    total = 0;
    useful_tweets = [];
    #removing spam
    for t in tweets:
        analyze = tb(t.text);
        if analyze.polarity == 0 or analyze.subjectivity == 0:
            tweets.remove(t);
        elif analyze.subjectivity >= .5:
            #if analyze.polarity >= .5 or analyze.polarity <= -.5:
            useful_tweets.append(t);
    for t in useful_tweets:
        analyze = tb(t.text);
        total += analyze.polarity;
    
    concensus = total/len(useful_tweets);
    print("CONCENSUS: %.4f\n" % concensus);
    if concensus > .75:
        print("STRONG BUY");
    elif concensus > .5 and concensus < .75:
        print("BUY");
    elif concensus > .25 and concensus < .5:
        print("WAIT BEFORE YOU BUY");
    elif concensus > -.25 and concensus < .25:
        print("DO MORE RESEARCH");
    elif concensus > -.5 and concensus < -.25:
        print("DISCOURAGE BUYING NOW");
    elif concensus > -.75 and concensus < -.50:
        print("DON'T BUY");
    elif concensus < -.75:
        print("AVOID LIKE THE PLAGUE");
        
def saveChart(tickerSymbol, startDate, endDate):
    #ticker name schemes
    filename = tickerSymbol + ".csv";
    #create file
    df = web.DataReader(tickerSymbol, "yahoo", startDate, endDate);
    df.to_csv(filename);
    return df;

def buildGraph(df, tickerSymbol):
    #plot csv
    ax = plt.gca()
    df.plot(kind='line',y='Adj Close',ax=ax);
    df.plot(kind='line',y='High',ax=ax);
    df.plot(kind='line',y='Low',ax=ax);
    plt.show()
    #print current stock price
    print("Current Price: $%.2f" % si.get_live_price(tickerSymbol));

def main():
    #datatime.datetime is a data type within the datetime module
    d = datetime.datetime.today();
    start = datetime.datetime(2019, 7, 10);
    end = d;
    #enter the current ticker symbol
    ticker = input("Enter The Ticker Symbol>>> ");
    df = saveChart(ticker, start, end);
    buildGraph(df, ticker);
    #sentiment analysis
    #tweets = getTweets(ticker);
    #analyzeTweets(tweets);
    
if __name__ == "__main__":
    main();