import datetime
import tda
import pandas as pd
from tda import auth, client
from tda.orders.equities import equity_buy_limit, equity_buy_market, equity_sell_limit, equity_sell_market
from tda.orders.common import Duration, Session
import json
import config

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
#some index trade symbols are funky - use $SPX.X for SPX, etc
trade_symbol = '$SPX.X'

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
ocdf[['putCall', 'symbol', 'description', 'bid', 'ask', 'last', 'mark',
       'bidAskSize', 'lastSize', 'highPrice', 'lowPrice', 'openPrice',
       'closePrice', 'totalVolume', 'tradeDate', 'netChange', 'volatility',
       'delta', 'gamma', 'theta', 'vega', 'openInterest', 'timeValue',
       'theoreticalOptionValue', 'theoreticalVolatility', 'strikePrice',
       'expirationDate', 'daysToExpiration', 'expirationType',
       'lastTradingDay', 'percentChange', 'markChange', 'markPercentChange',
       'intrinsicValue', 'inTheMoney']]
# #ocdf.drop(['exchangeName', 'bidSize', 'askSize', 'tradeTimeInLong', 'quoteTimeInLong', 'rho', 'optionDeliverablesList', 'multiplier', 'settlementType', 'deliverableNote', 'isIndexOption', 'nonStandard', 'pennyPilot','mini'], axis='columns', inplace=True)
print(ocdf.columns)


