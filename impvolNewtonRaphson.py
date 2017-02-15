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

######################################################################
# Define function d_BSEuropeanOption
######################################################################
# This function returns the derivative with respect to sigma of the
# Black-Scholes European option price (i.e. vega). It is the derivative 
# of the BSEuropeanOptionfunction. It's the same for calls/puts.
#
 
def d_BSEuropeanOption(S, K, vol, r, t, q):
    from math import log, sqrt, exp, pi
    
    d1 = (log(S/K)+(r-q+(vol**2)/2)*t)/vol/sqrt(t)
    d2 = d1-vol*sqrt(t)
    dd1 = ((vol**2)*t*sqrt(t)-(log(S/K)+(r+vol**2/2)*sqrt(t)))/(t*vol**2)
    dd2 = dd1 - sqrt(t)
    df = S*exp(-q*t)*(1/sqrt(2*pi)*exp(-d1**2/2))*dd1-K*exp(-r*t)*(1/sqrt(2*pi)*exp(-d2**2/2))*dd2
    return df

######################################################################
# Define function NewtonRaphson
######################################################################
# This function takes:
# f: a function
# df: the derivative of that function
# xn: an estimate of the root of the function
# xtol: the precision required in the value of the root
#
# This function returns:
# The root to the function supplied, using the Newton-Raphson method.
#
def NewtonRaphson(f, df, xn, xtol):
    fxn = f(xn)
    dfxn = df(xn)
    i = 1
    while (abs(fxn/dfxn)>xtol):
        xn = xn - fxn/dfxn
        fxn = f(xn)
        dfxn = df(xn)
        i = i + 1
    return xn

#############################################################################
# Define function 'impvolNewtonRaphson'
#############################################################################
# The function uses the Newton-Raphson root-finding method to find the
# implied volatility, i.e. the vol which makes the price according to 
# Black-Scholes, less the actual option price, equal to zero:
#           BS_European_Call(S,K,vol,r,t) - C = 0
#                       or:
#           BS_European_Put(S,K,vol,r,t) - P = 0
#
# Inputs:
# C = the option price
# S = the price of the underlying asset
# K = the option strike price
# r = the risk free rate
# t = the time to maturity of the option (in years)
# q = the annual dividend yield of the underlying
# call = True: the option is a call option, or else it is a put option
# xn = an initial guess at the implied volatility 
# xtol = the tolerance in the returned value for implied volatility
# 
# Outputs:
# vol = the implied annual volatility of the underlying asset
                          
def impvolNewtonRaphson(C, S, K, r, t, q, xn, xtol, call):
    from math import exp
# If we are dealing with a call option:
    if (call==True): 
    # Calculates rational price bounds for a call option per Merton (1973):
        lowerC = S - K*exp(-r*t)
        upperC = S
        if (C>upperC):
            print('Supplied C is above rational price bound')
            return -1
        elif (C<lowerC):
            print('Supplied C is below rational price bound')
            return -1
        else:
        # The supplied C is good, so we call the Newton-Raphson function to
        # find the implied volatility:
        # Defines the function we are trying to find the root of
            f = lambda vol: BSEuropeanOption(S, K, vol, r, t, q, call) - C
        # Defines the derivative of the function we are trying to find the root of
            df = lambda vol: d_BSEuropeanOption(S, K, vol, r, t, q)
        # Uses the function and its derivative to find the root using the
        # Newton-Raphson method
            vol = NewtonRaphson(f, df, xn, xtol)
            return vol
    elif (call==False):
    # Calculates rational price bounds for a put option per Merton (1973):
        lowerP = K*exp(-r*t) - S
        upperP = K
    if (C>upperP):
        print('Supplied P is above rational price bound')
        return -1
    elif (C<lowerP):
        print('Supplied P is below rational price bound')
        return -1
    else:
        # The supplied P is good, so we call the Newton-Raphson function to
        # find the implied volatility:
        f = lambda vol: BSEuropeanOption(S, K, vol, r, t, q, call) - C
        # Defines the derivative of the function we are trying to find the root of
        df = lambda vol: d_BSEuropeanOption(S, K, vol, r, t, q)
        # Uses the function and its derivative to find the root using the
        # Newton-Raphson method
        vol = NewtonRaphson(f, df, xn, xtol)
        return vol

#############################################################################
# Test functions with some arbitrary values
#############################################################################
# Test parameters:
S = 100
K = 100
vol = 0.25
r = 0.05
t = 0.1
q = 0.02
call = False
xn = 0.5
xtol = 10**-5

# Calling the functions using these parameters
price = BSEuropeanOption(S, K, vol, r, t, q, call)
impVol = impvolNewtonRaphson(price, S, K, r, t, q, xn, xtol, call)

if call == True:
    optiontype = "call"
else:
    optiontype = "put"
    
print('''The price of a European %s option for S = %4.2f, K = %4.2f, 
      vol = %4.3f, r = %4.3f, t = %4.3f, q = %4.3f is %4.3f'''
      % (optiontype, S, K, vol, r, t, q, price))
print('''The volatility implied by a European %s option price of %4.3f, and
      S = %4.2f, K = %4.2f, r = %4.3f, t = %4.3f, q = %4.3f is %4.3f'''
      % (optiontype, price, S, K,  r, t, q, impVol))


