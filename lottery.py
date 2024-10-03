import random
import copy
import helpers as hlpr
def is_lottery(lottery):
    """ returns true if lottery probabilities sum to near 1 and are all non-negative,
        lottery = [event-1, ..., event-n]
                   event-k = {"out": float_value, "prob": float_value}
    """
    total_prob = 0.0
    for event in lottery:
        if event['prob'] < 0.0: return False  #TODO fix for precision error
        total_prob += event['prob']
    if hlpr.is_near_target(total_prob, target = 1, precision = .000001):
        return True
    else:
        return False


def print_lottery(lottery):
    """prints out a lottery in more readable form
       TODO:  only goes 2 deep
    """
    TAB = "    "
    for k, event in enumerate(lottery):
        if type(event['out']) == list:
            print(f"event {k} prob = {event["prob"]:.3f} outcome = lottery")
            for j, subevent in enumerate(event['out']):
                print(f"{TAB}event {j} prob = {subevent["prob"]:.3f} outcome = {subevent["out"]}")
        else:
            print(f"event {k} prob = {event["prob"]:.3f} outcome = {event["out"]}")


def print_lottery_with_utility(lottery, u):
    """prints out a lottery in more readable form
       TODO:  only goes 2 deep
    """
    TAB = "    "
    print("Lottery")
    for k, event in enumerate(lottery):
        outcome = event['out']
        if type(outcome) == list:
            print(f"event {k} prob = {event["prob"]:.3f} outcome = lottery")
            for j, subevent in enumerate(outcome):
                subout = subevent["out"]
                print(f"{TAB}event {j} prob = {subevent["prob"]:.3f} outcome = {subout},utility = {u(subout):.4f}")
        else:
            print(f"event {k} prob = {event["prob"]:.3f} outcome = {event["out"]}, utility = {u(outcome):.4f}")


def print_lottery_list(lot_list):
    print(f"Lottery list has {len(lot_list)} lottery(s)")
    for k, lottery in enumerate(lot_list):
        print(f"Lottery {k}")
        print_lottery(lottery)
    print()


def input_lottery():
    """Builds a lottery from user input
       TODO:  loop until valid lottery entered
    """
    lottery = []
    num_events= hlpr.input_number("Enter number of events")
    for k in range(num_events):
        event = {}
        print(f"   Event {k+1}")
        outcome = hlpr.input_number("Enter outcome")
        prob = hlpr.input_number("Enter probability")
        event['out'] = outcome
        event['prob'] = prob
        lottery.append(event)
    if is_lottery(lottery):
        return lottery
    

def make_simple_lottery(min_pay = 0, max_pay = 100, 
                        num_events = 2):
    """Builds a random simple lottery.
    Parms:
    min_pay, integer, lower bound on outcome,
    max_pay, integer, upper bound on outcome,
    num_events, integer, number of events in lottery

    Returns:
    lottery = [event_1, ..., event_num_events]
    event_k = {'out': pay, 'prob': probability
    """     
    lottery = []
    total_prob = 0
    upper_prob = 1.0
    for k in range(num_events-1):
        event = {}
        event['out'] = float(random.randint(min_pay, max_pay))
        prob = random.uniform(0.0, upper_prob)
        event['prob'] = prob
        upper_prob -= prob
        lottery.append(event)
    event = {}
    event['out'] = float(random.randint(min_pay, max_pay))
    event['prob'] = upper_prob
    lottery.append(event)
    if is_lottery(lottery):
        return lottery
    else:
        print("function make_simple_lottery failed to make lottery")
        make_simple_lottery()


def might_make_compound_lottery(lottery, min_pay = 0, 
                                max_pay = 100, num_events = 2, 
                                prob_compound_event = .5):
    """For each event in a simple lottery, turn that event's outcome into a lottery with prob_compound_event
    """
    new_lottery = [ ]
    for event in lottery:
        if random.random() <= prob_compound_event:
            lot = make_simple_lottery(min_pay = min_pay, max_pay = max_pay,
                                       num_events = num_events)
            new_event = {}
            new_event['out'] = lot
            new_event['prob'] = event['prob']
        else:
            new_event = event
        new_lottery.append(new_event)
    return new_lottery


def make_simple_lottery_list(num_lotteries = 2, min_pay = 0, max_pay = 100, 
                          min_events = 2, max_events = 2):
    """Builds a random list of lotteries
    
        Lottery payoffs are random draws beteen min_pay and max_pay,
        Lottery probabilities are random uniform draws that sum to one.
    
        args:
            number = int > 0, number of lotteries in list.
            payoff in [min_pay, max_pay]
            num_events in [min_events, max_events]
    """
    lottery_list = []
    for num_lot in range(num_lotteries):
        num_events = random.randint(min_events, max_events)
        lottery = make_simple_lottery(min_pay = min_pay, max_pay = max_pay, num_events = num_events)
        lottery_list.append(lottery)
       
    return lottery_list


def make_compound_lottery_list(num_lotteries = 2, 
                               min_pay = 0,
                               max_pay = 100, 
                               min_events = 2, 
                               max_events = 2,
                               prob_compound_event = .5): 
    """Builds a random list of lotteries
    
        Lottery payoffs are random draws between min_pay and max_pay,
        Lottery probabilities are random uniform draws that sum to one.
    
        args:
            number = int > 0, number of lotteries in list.
            compound = bool, if True allows compound lotteries one deep,
            negative = bool, if False min_pay = 0, if True min_pay = -max_pay.

        This works for  a  compound lottery of depth 2, i.e., a lottery with an event that is also a lottery.
        TODO: make this work for any finite depth.
    """
    lottery_list = make_simple_lottery_list(num_lotteries = num_lotteries,
                                                        min_pay = min_pay, 
                                                        max_pay = max_pay, 
                                                        min_events = min_events,
                                                        max_events = max_events)
    lot_list = []
    for lottery in lottery_list:
        num_events = random.randint(min_events, max_events)
        lot = might_make_compound_lottery(lottery, min_pay = min_pay,
                                          max_pay = max_pay, num_events = num_events,
                                          prob_compound_event = .5)
        lot_list.append(lot)
    return lot_list


def reduce_lottery(lottery):
    """ Reduces compound lottery to a simple lottery.
    
        A compound lottery has sub-lotteries as outcomes.
        A simple lottery only has payoffs as outcomes.
        
        args:
            lottery, list of dictionaries.
        returns:
            simple_lottery, list of dictionaries with no sub-lottery.
        This should work for arbitrayry depth of compound lotteies but has 
            only been tested on a depth of 2.
        TODO: Test this on arbitrary depths once compound builder can do this.
    """
    compound = True
    test_lottery = copy.deepcopy(lottery)
    while compound:
        compound = False
        new_lottery = []
        for event in test_lottery:
            if type(event['out']) == list:
                for subevent in event['out']:
                    new_event = {}
                    new_event['out'] = subevent['out']
                    if type(subevent['out']) == list: 
                        compound = True
                    new_event['prob'] = event['prob']*subevent['prob']
                    new_lottery.append(new_event)
            else:
                new_lottery.append(event)
        if compound == True: 
            test_lottery = copy.deepcopy(new_lottery)
    return new_lottery


if __name__ == "__main__":   
    import utility_functions as utils
    lottery = [{'out': 25.0, 'prob': 0.9553673849996607},
               {'out': 59.0, 'prob': 0.044632615000339326}]
    print("This is a lottery")
    print_lottery(lottery)
    print("is this a lottery?")
    print(is_lottery(lottery))
    print()
    
    # un-comment lines below if you want to test input_lottery()
    #lottery = input_lottery()
    #print(lottery)

    print("This is a lottery, along with the utility of the lottery")
    print_lottery_with_utility(lottery, utils.crra_utility)
    print()
    
    print("Now we will make some lottereis using the make functions")
    print("simple lottery with five events using make_simple_lottery")
    lot = make_simple_lottery(num_events = 5)
    print_lottery_with_utility(lot, utils.crra_utility)
    print()

    print("make a compound lottery from the lottery above")
    c_lot = might_make_compound_lottery(lot)
    print_lottery_with_utility(c_lot, utils.crra_utility)
    print()

    print("make a list of simple lotteries")
    lottery_list = make_simple_lottery_list(num_lotteries= 4, max_events = 4)
    print_lottery_list(lottery_list)
    print()

    print("make a list of compound lotteries")
    lot_list = make_compound_lottery_list(num_lotteries = 5,
                                      min_pay = 0,
                                      max_pay = 100,
                                      min_events = 2,
                                      max_events = 4,
                                      prob_compound_event = .5)
    print_lottery_list(lot_list)
    print()  

    print("reducing the compound lotteries in the last list")
    reduced_lot_list = []
    for lottery in lot_list:
        reduced_lottery = reduce_lottery(lottery)
        reduced_lot_list.append(reduced_lottery)
    print_lottery_list(reduced_lot_list) 
    print()