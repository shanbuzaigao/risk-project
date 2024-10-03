import lottery as lot
import helpers as hlpr
def expected_value(lottery):
    """Calculate expected value of a lottery
    
        arg:
            lottery, list of dictioaries
        
        returns:
            ev, float, expected value of the lottery
    """
    new_lottery = lot.reduce_lottery(lottery)
    ev = 0.0
    for node in new_lottery:
        if type(node['out']) == type([]):
            # make recursive call to evaluate sub-lottery
            ev = node['prob'] * expected_value(node['out'])
        else:
            ev = ev + node['prob'] * node['out']
    return ev


def expected_utility(lottery, util):
    """Calculate expected utility of a lottery
    
        arg:
            lottery, list of dictioaries containing 
                     keys, values {'prob': pr, 'outcome': out}
                         pr, float between 0.0 and 1.0 inclusive
                         out, either another lottery or a float payoff
                     
            u, utility function, returns utility of a payoff outcome
        
        returns:
            eu, float, expected utility of the lottery
    """
    eu = 0.0
    new_lottery = lot.reduce_lottery(lottery)
    for event in new_lottery:
            eu += util(event['out'])*event['prob']
    return float(eu)


def certainty_equivalent(lottery, u, min_x, max_x, precision = .1):
    """ Returns the certainty equivalent (ce) of a lottery.
    
        u(ce) = expected_utility(lottery, u)
        
        args:
            lottery, list of dictionaries.
            u, utility function defined over payoffs in dictionaries
        returns:
            ce, float, certainty equivalent
        TODO: only tested on linear_utility, needs to be tested with other utility functions
    """
    eu = expected_utility(lottery, u)
    print(f"expected utility = {eu:.4f}")
    # now do a bisection search for x such that u(x) = eu
    lower_bound = min_x
    upper_bound = max_x
    num_trys = 0
    while(True):
        num_trys += 1
        u_upper = u(upper_bound)
        u_lower = u(lower_bound)
        try_this = .5*lower_bound + .5*upper_bound
        u_try = u(try_this)
        #print(f"lb = {lower_bound}, try = {try_this}, ub = {upper_bound}")
        #print(f" eu = {eu}, u({try_this}) = {u_try}")
        if hlpr.is_near_target(u_try, target = eu, precision = precision):
            return try_this, u_try, eu, num_trys 
        if u_try < eu:
            lower_bound = try_this
        else:
            upper_bound = try_this


def risk_premium(lottery, ce):
    """ Returns the risk premium (rp) of a lottery.
    
        rp = expected_value(lottery) - certainty_equivalent(lottery, u)
        
        args:
            lottery, list of dictionaries.
            u, utility function defined over payoffs.
        returns:
            rp, float, risk premium
    """
    return expected_value(lottery) - ce


def lottery_choice(lottery_list, u):
    """ Choose the lottery with the highest expected utility
        from lottery_list using utility function u.
        
        returns:
            lottery_index, eu  expected utility of the lottery
    """
    lottery_index = None
    list_of_expected_u = []
    for lottery in lottery_list:
        lottery_utility = expected_utility(lottery, u)
        list_of_expected_u.append(lottery_utility)
    eu = max(list_of_expected_u)
    lottery_index = list_of_expected_u.index(eu)
    return lottery_index, eu


if __name__ == "__main__":
    import lottery as lot
    import utility_functions as uf
    from functools import partial

    lottery = [{'out': 100, 'prob': 0.5}, 
               {'out': 50, 'prob': 0.25}, 
               {'out': 50, 'prob': 0.25}]
    lot.print_lottery(lottery)
    print(f"Expected value = {expected_value(lottery)}.")
    print(f"Expected utility = {expected_utility(lottery, uf.crra_utility)}.")
    print()

    min_pay = 0
    max_pay = 1000
    precision = 1
    lottery =  lot.make_simple_lottery(min_pay = min_pay, max_pay = max_pay, num_events = 5)
    lot.print_lottery_with_utility(lottery, uf.hara_utility)

    for k in range(5):
        precision = precision * .1
        ce, u_ce, eu, trys = certainty_equivalent(lottery, uf.hara_utility, min_pay, max_pay, precision)
        print(f"pre = {precision:.6f}, ce = {ce:.4f}, diff = {u_ce-eu:.6f}")
        print(f"ce = {ce:.4f}, u(ce) = {u_ce:.4f}, num_trys = {trys}")
    print()

    lot_list = lot.make_compound_lottery_list(num_lotteries = 5,
                                      min_pay = 0,
                                      max_pay = 100,
                                      min_events = 2,
                                      max_events = 4,
                                      prob_compound_event = .5)
    lot.print_lottery_list(lot_list)
    for k in range(1, 10):
        util = partial(uf.crra_utility, r = k/10)
        print(f"crra utility with r = {k/10}")
        for k, lottery in enumerate(lot_list):
            print(f"Lottery {k} has ev = {expected_value(lottery):.4f} and eu = {expected_utility(lottery, util):.4f}")
        print()
    
    lot_list = lot.make_compound_lottery_list(num_lotteries = 5,
                                          min_pay = 0,
                                          max_pay = 100,
                                          min_events = 2,
                                          max_events = 4,
                                          prob_compound_event = .5)
    lot.print_lottery_list(lot_list)
    lot_choice = lottery_choice(lot_list, uf.crra_utility)
    print(lot_choice)
    print()

    for k, lottery in enumerate(lot_list):
        str_out = f" lottery {k} has expected value = {expected_value(lottery):.4f}"
        str_out += f" and expected utility = {expected_utility(lottery, uf.crra_utility):.4f}"
        print(str_out)
    print()
