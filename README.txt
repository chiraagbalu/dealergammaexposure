this is for determining dealer gamma exposure, as well as the zero gamma point - mainly for indices!

what is dealer gamma exposure?

dealer gamma exposure is the amount of option gamma that option dealers are exposed to at any given price for a certain
security.
let's break that down.

basically, when people sell stock options, they profit when the option loses value.

what is an option?
options are derivatives of an underlying security.
calls are a contract giving the owner the right to buy 100 shares at a strike price until/at an expiration date.
puts are a contract giving the owner the right to sell 100 shares at a strike price until/at an expiration date.

how much do they cost?
it depends.
let's start by analyzing option cost at expiration - its the easiest to understand.
at expiration, if an underlying security is higher than the value of the call option's strike price, the option will
turn a profit if exercised.
for example, a 200 strike call for a security trading 210 at expiration would give the right to buy 10 dollars under
market price.
if this right is exercised, the shares can be resold to the market at market price.
this would mean someone would get (210-200) for each share, 100 per contract.
this works out to 1000 dollars per contract.

knowing how much an option is worth before expiration hinges on understanding the above.
this is because options are priced based on how much they could be worth at expiry.
we can think of a security's current price, volatility, and the amount of time until the option's expiry date as
creating a distribution of possible prices at expiry.
for each of these possible prices, we can calculate how much the option is worth at expiry.
we can also find a rough probability that the stock ends at any of these given prices.
with the above, we can multiply the probability of each price at expiry, times the amount the option would be worth,
to get an 'expected value' for the option.

as previously mentioned, this distribution is based on the current price, volatility, and time until expiration.
with more time until expiration, the distribution is wider, as the stock has more time to travel to a profitable price.
this effect is known as theta, the option price sensitivity to time until expiration of the option.
if a security is more volatile, the distribution also becomes wider, since the security can travel further in price
with the same amount of time.
this effect is known as vega, the option price sensitivity to volatility of the underlying security.
finally, when the current price of the underlying changes, the distribution of future possible prices shifts up and
down.
when the price goes up, the distribution shifts upwards, meaning a call option is more likely to be in profit - and
vice versa.
this effect is known as delta, the option price sensitivity to the price of the underlying security.

so why do people sell options?

people sell options so that they can profit when the option loses value - we call them dealers.
their favorite way to make money is through theta decay - the loss in time value of an option as it gets closer to
expiring.
as a quick recap, the option loses value when time passes because the distribution of prices it can reach tightens,
decreasing the probability of the option being profitable at expiration.

how do they profit off just theta, aren't there other factors?

there are! but option dealers don't want to be exposed to any other factors in option pricing - specifically
the underlying's price and volatility. (we aren't covering the volatility part of the equation)
to offset the effect of the underlying price movement, option dealers buy and sell shares of the underlying to
hedge their position- impacting the underlying market.
if an option dealer sells a call, they are effectively short the underlying security, as they'd profit if the security
went down.
since they don't want to be exposed to directional risk at all, they can buy shares of the underlying security to offset
their option they sold.

how much do they buy and sell?

by using delta, the option price sensitivity to the underlying security's price, they can calculate how many shares
to be long.
when an option has a delta of 0.2, it means that the contract price changes $0.2 for each $1 movement in the underlying.
so since an option works in 100 shares per contract, being short a 0.2 delta call is the roughly the same as being
short 20 shares.
to offset this, an option dealer can buy 20 shares and be directionally neutral - only profiting off of theta now.

won't delta change over time?

it will! delta isn't static - it changes over the life of an option.
it also changes based on volatility, time, and price of the underlying, just like the option itself.
options that wouldn't be profitable at expiry depend on volatility and time to have any value.
they only are worth anything because of the possibility they could be valuable at expiry.
this means that the specific price of the underlying doesn't impact their price as much - and they trade less like their
underlying security.
if they trade less like their underlying security, their delta is closer to 0, as a $1 move in the underlying changes
the option price less.
delta changes when the underlying security price changes - as price increases, a call that wouldn't be profitable
starts to care more about the price of the underlying, increasing its delta.
the sensitivity of delta to change in underlying price is known as gamma.
yes. we've finally made it to gamma.

why do we care about gamma again?
we care about gamma because when the delta of an option position changes, the dealer has to re-hedge their position.
the re-hedging of the position impacts the underlying market - and we want to be able to predict this ahead of time.

how do they hedge based on their position and underlying movement?
if dealers are long calls, they're long x deltas, and have to short shares to be delta neutral.
when the underlying moves up, delta increases, and they're long more deltas, so they short more shares to be neutral.
when the underlying moves down, delta decreases, and they're long less deltas, so they buy more shares to be neutral.

if dealers are short calls, they're now short x deltas, and have to buy shares to be delta neutral.
when the underlying moves up, delta increases, and they're short more deltas, so they buy more shares to be neutral.
when the underlying moves down, delta decreases, and they're short less deltas, so they short more shares to be neutral.

apply the above to puts, etc

how much are they buying/selling at certain areas?
gamma is strongest when the underlying is close to the strike price, even a $0.01 change has a large impact
on whether the option will be profitable.
this means that dealers are buying and selling more shares over smaller distances in price.
this means that there's more liquidity in these areas of the market.
we can almost think of liquidity in this case as resistance to price change.
high gamma exposure means dealers are net providing liquidity to the market, and negative gamma exposure means they are
net taking liquidity from the market.
this is the reason that, on key expirations (monthly, quarterly, even weekly), markets seem to 'pin' to certain strikes.
estimating gamma exposure will let us know this kind of stuff ahead of time can make us money.

ok so how do we calculate it?
when we calculate gamma exposure, we assume that dealers are long calls and short puts - generally true for indices.
as mentioned earlier, gamma can cause dealers to provide or take liquidity in certain areas (buying/selling shares)
since they would be long calls and short puts in general, we can assume that calls will carry positive gamma exposure
and puts will carry negative gamma exposure.

each option's gamma contribution is:
gamma * contract size * open interest (open positions) * underlying price * (put/call modifier: -1 if put, 1 if call)
the above gives option change in delta per 1 point move in the index.
if we want percent, we multiply by 0.01*underlying price,
gamma * contract size * open interest (open positions) * underlying price^2 * (p/c modifier) * 0.01
our assumptions generally overestimate dealer gamma exposure, since investors sometimes also long calls for leverage,
sell puts for yield, and trade spreads/option combinations.

we can use the above equation to find the gamma exposure for each strike at the currently underlying price.
but that doesn't help us approximate gamma exposure when the market moves - which is what we really wanted.
for this, we will need to calculate how the option gammas are going to change and what they'll be for each underlying
price. for every option.
yay.
for this, we get to use the famous financial engineering equation - Black-Scholes.
Black-Scholes is basically just a mathematical equation for pricing options - we covered its factors earlier.
its a differential equation, so we solve for gamma and compute it (won't go into math just trust me and by extension
wikipedia)
putting all of the gamma exposures at each price for each strike gives us a full picture of the gamma profile for
each expiration date, we did it!



risk free interest rate (10y yield): 1.97%




