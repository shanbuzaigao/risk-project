import math
import matplotlib.pyplot as plt

def linear_utility(m, intercept=0, slope=1.0):
    """linear utility of money
    
        args: m, float, amount of money.
              a, float, intercept of line.
              b, float, slope of line.
              
        returns: util, float, utility of money m.    
    """
    util = intercept + slope*m
    return float(util)

def cara_utility(m,r=0.005):
    """Constant Absolute Risk Aversion"""
    util = 1 - (math.e)**(-r*m)
    return float(util)

def crra_utility(m,r=0.5):
    """Constant Relative Risk Aversion"""
    if r == 1:
        util=math.log(m)
    if r != 1:
        util=(m**(1-r)-1)/(1-r)
    return float(util)

def exponential_utility(m, a=.005):
    util = 1.0-math.e**(-a*m)
    return float(util)

def hara_utility(m, a=2, b=50):
    """Hyperbolic Absolute Risk Aversion"""
    if a == 0:
        util = exponential_utility(m, 1/b)
    elif b == 0:
        util = cara_utility(m, 1/a)
    else:
        r=1/a
        c= -b/a
        util = ((m - c)**(1-r))/(1-r)
    return float(util)


def plot_utility(utility, utility_name):
    """ plot utility function utility
        where name is what you want to call it"""
    x = []
    y = []
    for i in range(1, 1001):
        x.append(i)
        y.append(utility(i))
    plt.plot(x,y)
    plt.legend([utility_name])
    plt.show()


if __name__ == "__main__":
    print(hara_utility(10))
    utils =[linear_utility, cara_utility, crra_utility, exponential_utility, hara_utility]
    plot_utility(crra_utility, "crra")