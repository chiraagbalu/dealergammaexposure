import datetime as dt
import tda
import numpy as np
import scipy
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
from tda import auth, client
from tda.orders.equities import equity_buy_limit, equity_buy_market, equity_sell_limit, equity_sell_market
from tda.orders.common import Duration, Session
import json
import config
import asyncio

#set up client!
try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    s = Service('/Users/chiraagbalu/PycharmProjects/tdarobot/chromedriver')
    with webdriver.Chrome(service=s) as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)

acct_id = 123456789

#getting data
#some index trade symbols are funky - use $SPX.X for SPX, etc
tradesymbolSPX = '$SPX.X'
print('input the symbol you want gamma exposure +_option levels for!')
trade_symbol = input()
symbolCandles = c.get_price_history(trade_symbol, start_datetime=(dt.datetime.now()-dt.timedelta(days=2)), need_extended_hours_data=False).json()
#get last spot price
spot = symbolCandles['candles'][-1]['close']
print(spot)
#we're going to make a dataframe of the options chain to make it easier to access certain values
option_chain_dict = []
query = c.get_option_chain(trade_symbol).json()
#use both puts and calls
for put_call in ['callExpDateMap', 'putExpDateMap']:
    #make dictionary of contracts where keys are expirations
    contract = dict(query)[put_call]
    expirations = contract.keys()
    #use every expiry
    for expiry in list(expirations):
        # take the strikes at each expiry
        strikes = contract[expiry].keys()
        #use every strike in the chain
        for strike in list(strikes):
            #add each strike's information to the option chain dictionary
            entry = contract[expiry][strike][0]
            option_chain_dict.append(entry)
option_chain_df = pd.DataFrame(option_chain_dict)
#keep original, work with easy name
ocdf = option_chain_df.copy(deep=False)
#get the columns we actually need
allstrikegammadf = ocdf[['putCall', 'symbol', 'strikePrice', 'gamma', 'totalVolume',  'openInterest',  'daysToExpiration', 'expirationDate']]
#sort to strikes within 10% of spot price
gammadf = allstrikegammadf[allstrikegammadf['strikePrice'].between(spot*0.9, spot*1.1)]

calldf = gammadf.loc[gammadf.putCall == 'CALL']
putdf = gammadf.loc[gammadf.putCall == 'PUT']

#making things floats for calculation
calldf['gamma'] = calldf['gamma'].astype(float)
calldf['openInterest'] = calldf['openInterest'].astype(float)
putdf['gamma'] = putdf['gamma'].astype(float)
putdf['openInterest'] = putdf['openInterest'].astype(float)

#calculating raw gamma exposure for all calls
gammadf['RAWcallGEX'] = calldf['gamma'] * calldf['openInterest'] * spot * 100

#calculating callGEX per 1% move in underlying
gammadf['callGEX'] = gammadf['RAWcallGEX'] * 0.01 * spot

#calculating raw gamma exposure for all puts
gammadf['RAWputGEX'] = putdf['gamma'] * putdf['openInterest'] * spot * 100 * -1

#calculating putGEX per 1% move in underlying
gammadf['putGEX'] = gammadf['RAWputGEX'] * 0.01 * spot

#calculating totalGEX per 1% move in underlying
gammadf['totalGEX'] = (gammadf['callGEX'].fillna(0) + gammadf['putGEX'].fillna(0))
totalGEX = gammadf['totalGEX'].sum()
print('total GEX = {:,}'.format(totalGEX))


#sorting by strike
strikeGammas = gammadf.groupby(['strikePrice']).sum()
#print(strikeGammas.sort_values(by='openInterest', ascending=False))

nearestExp = gammadf[gammadf['daysToExpiration'] == gammadf['daysToExpiration'].min()]
nearestExp = nearestExp[['strikePrice', 'openInterest', 'gamma', 'totalVolume']]
nearestEXP = nearestExp[(nearestExp != 0).all(1)]
nearestByOI = nearestExp.sort_values(by='openInterest', ascending=False)
nearestByGamma = nearestExp.sort_values(by='gamma', ascending=False)
nearestByVolume = nearestExp.sort_values(by='totalVolume', ascending=False)
topOI = nearestByOI[:3]
topGamma = nearestByGamma[:3]
topVolume = nearestByVolume[:3]
print('top Open Interest Strikes')
print('strike: ')
print(topOI['strikePrice'].to_string(index=False))
print('oi: ')
print(topOI['openInterest'].to_string(index=False))
print('top Gamma Strikes')
print('strikes: ')
print(topGamma['strikePrice'].to_string(index=False))
print('gamma: ')
print(topGamma['gamma'].to_string(index=False))
print('top Volume Strikes')
print('strike: ')
print(topVolume['strikePrice'].to_string(index=False))
print('volume: ')
print(topVolume['totalVolume'].to_string(index=False))

#print(nearestExp['daysToExpiration'])


#calculating gamma using black-scholes equation
#S = underlying spot price
#K = strike price
#vol = implied volatility
#T = time until expiration
#r = risk free interest rate
#q = dividend yield
#OI = open interest
#credit to wikipedia for the equation

#assume dividend is 0
#assume risk free interest rate is 2%
riskFreeRate = 0.02

def calcGamma(S, K, vol, T, r, q):
    #we have T and vol in denominator so if its 0 we need to screen for that - gamma will be 0 if either are 0
    if T == 0 or vol == 0:
        return 0
    #black scholes equation to find d1
    d1 = (1/vol*(np.sqrt(T)))*(np.log(S/K) + (r-q+(0.5*vol**2))*(T))
    #calculating gamma from d1
    gamma = norm.pdf(d1)/(S*vol*np.sqrt(T))
    return gamma

def calcGammaExposure(S, K, vol, T, r, q, OI):
    return calcGamma(S, K, vol, T, r, q) * 100 * OI * (S**2) * 0.01



