#!/usr/bin/python3
import sys

def find_gifts(prices, balance):
    '''
    Finds two distinct gifts given PRICES whose sum is minimally 
    under (or equal to) the gift card balance.
    '''
    if len(prices) < 2: # more than two gifts required
        return None 
    left, right = 0, len(prices) - 1
    optimal = []
    min_diff = float('inf')
    while left < right:
        sum_prices = prices[left][1] + prices[right][1]
        if sum_prices < balance:
            leftover = balance - sum_prices # how much funds are leftover, guaranteed to be > 0
            if leftover < min_diff:
                min_diff = leftover
                optimal = [prices[left], prices[right]]
            left += 1
        elif sum_prices == balance:
            return [prices[left], prices[right]]
        else:
            right -= 1
    return optimal

def output(gifts):
    '''
    Prepares the proper output to stdout based on our algorithm's output.
    '''
    if gifts:
        item1, item2 = gifts[0], gifts[1]
        output = item1[0] + " " + str(item1[1]) + ", " + item2[0] + " " + str(item2[1])
    else:
        output = "Not possible"
    return output

if __name__ == '__main__':
    # take in inputs
    if len(sys.argv) != 3:
        print("Invalid user input. Number of arguments isn't equal to 2 or the user inputs themselves are invalid.")
    else:
        text, balance = sys.argv[1], sys.argv[2]
        # validate/process args
        fp = open(text)
        prices = []
        for line in fp:
            gift, price = line.strip().split(', ')
            prices.append((gift, int(price))) 

        # print optimal gifts to stdout
        best_gifts = find_gifts(prices, int(balance))
        print(output(best_gifts))