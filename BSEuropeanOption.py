#############################################################################
# Define function BSEuropeanOption
#############################################################################
# This function takes S, K, vol, r, t, and q and returns the European 
# option price for a put or call according to the Black-Scholes formula
#
# Inputs:
# S = the price of the underlying asset
# K = the option strike price
# vol = the annual volatility of the underlying asset
# r = the risk free rate
# t = the time to maturity of the option (in years)
# q = the annual dividend yield of the underlying
# call = True: the option is a call option, or else it is a put option
#
# Outputs:
# The price of the call or put option

def BSEuropeanOption(S, K, vol, r, t, q, call):
    from scipy.stats import norm
    from math import log, sqrt, exp
        
    d1 = (log(S/K)+(r-q+(vol**2)/2)*t)/vol/sqrt(t)
    d2 = d1-vol*sqrt(t)
    
    if call == True:
        price = S*exp(-q*t)*norm.cdf(d1)-K*exp(-r*t)*norm.cdf(d2)
    else:
        price = K*exp(-r*t)*norm.cdf(-d2)-S*exp(-q*t)*norm.cdf(-d1)
        
    return price

#############################################################################
# Test function with some arbitrary values
#############################################################################
print(BSEuropeanOption(100, 100, 0.2, 0.05, 0.5, 0, True))
print(BSEuropeanOption(100, 100, 0.2, 0.05, 0.5, 0, False))