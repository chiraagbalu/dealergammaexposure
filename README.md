# instructions
## create a config.py file with the necessary variables to run this

- config.api_key, config.redirect_uri, config.token_path)


# description/explanation
in this project, we will determine the total gamma exposure for a selected security - and finding some important levels
currently debugging some symbols, definitely works for $SPX.X


## what is gamma exposure?


gamma exposure (GEX) is the amount of hedging that option market makers have to do on a symbol.
they will buy the dollar amount for each % change in the stock when GEX is positive, and sell when negative.
this allows us to know if the market will be self stabilizing or destabilizing.
generally speaking, GEX (gamma exposure) is always positive, so new flows help stabilize the market.
however, when GEX is relatively high, this stabilizing effect is stronger and compresses volatility.
when GEX is relatively low, dealers don't stabilize the market as much, allowing for larger swings in price.

## how does dealer hedging work?


how dealers initially hedge:
when dealers buy and sell options, they want their positions to be profitable.
however, they don't typically like to expose themselves to directional risk of a security, or how it's price movement
changes the option price.
delta is the sensitivity of an option's price to movement in the underlying, expressed as change in premium per $ change
in the underlying security.
as such, a 45 delta option basically has the same movement as 45 shares of the underlying.
to offset this directional risk, a dealer can short/buy shares based on delta and remain neutral.
this process is known as delta hedging.

how dealers change their hedges over time:
delta does not stay the same throughout the life of an option.
this means that option dealers need to continually adjust their hedges.
delta changes mainly due to volatility, time, and the price of the underlying.
the change in delta based on the change in underlying is known as gamma.
exposure to gamma is one of the key factors that cause options dealers to re-hedge their positions.
when gamma is high, they need to buy and sell more shares than when gamma is lower, leading to the described effects.


## how are the levels determined?


we take the option chain for the selected security, and look for the top 3 strikes for open interest, gamma, and volume.
high open interest/volume means that many positions are open on that strike, leading to a sort of 'pin' effect.
the pinning effect happens because when dealers have a lot of positions open at a strike, they aggressively hedge near
that price in order to keep their positions profitable.
this helps us know where the market could be likely to close, or magnet towards.
we also look at high levels of gamma for the same reason, higher gamma means dealers hedge more aggressively at those
prices.



