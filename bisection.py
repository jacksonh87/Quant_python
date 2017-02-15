#############################################################################
# Define function 'bisection'
#############################################################################
# This function takes:
# f: a function 
# a: a value to one side of a root to the function
# b: a value to the other side of a root to the function
# xtol: the precision required in the value of the root 
# and returns the root to the function
def bisection(f, a, b, xtol):
    fa = f(a)
    fb = f(b)

    if (fa*fb)>0:
        print("Wrong values. f(a) and f(b) must have opposite signs.")
        return -1
    else:
        xerr = abs(b-a)
        iter = 0
        m = (a+b)/2
        fm = f(m)
    while (xerr > xtol):
        iter = iter + 1
        if (fm == 0):
            xerr = 0
            return m
        elif (fm*fa)>0:
            a = m
        else:
            b = m
        xerr = abs(b-a)
        m = (a+b)/2
        fm = f(m)

    return m
   
    
#############################################################################
# Test function with some arbitrary values
#############################################################################
rootFunction = lambda x: x**2 - 1
a = 0
b = 10
xtol = 10**-5
print(bisection(rootFunction, a, b, xtol)) 
                     