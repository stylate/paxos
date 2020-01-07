## Question 2 - Gift Purchasing

### Concept

Given a gift card with a set balance `b`, we want to _*maximize*_ its usage by spending as much as possible on two separate gifts for two separate friends. Given an input file containing a sorted list of unique identifiers and their balances, we can produce an efficient O(n) algorithm that outputs the most expensive gifts that can be purchased with our gift card.

### Usage

All inputs should go in the `gift/inputs` folder. The rest of the code is as follows in `gift`. It is assumed that the user has python3 installed. All libraries used (`sys`, `unittest`) are built-in. Set the working directory as `gift` and run the following command:

```
python solution.py <input file> <balance>
```

Our first parameter should be a .txt file and be well-formed, the second parameter being a positive integer, an example being as follows:

```
Candy Bar, 500
Paperback Book, 700
Detergent, 1000
Headphones, 1400
Earmuffs, 2000
Bluetooth Stereo, 6000
```

An example input should be `python solution.py inputs/prices.txt 10000`. An example output would appear as:

```
Earmuffs 2000, Bluetooth Stereo 6000
```

For testing, run `test_solution.py` by entering the command `python test_solution.py`. 

### Algorithm

Our following assumptions are as follows:

- Every item is unique in its identifier (prices can be non-unique).
- Our input list is sorted by price.
- We can only buy one of each item.
- An item's price is a strictly positive integer.
- Our input file is well-formed (each line follows the structure "(Unique Identifier), (Price)").

Recall that our list is sorted by price, and that we want to maximize the balance given in our gift card. To do this, we use a two-pointer approach with the pointers `left` and `right` such that `left` points to the first index and `right` points to the last index of our array `prices`. For *simplicity* of explanation, consider `prices` to be an array of item costs (without keeping in mind of the unique identifier). In order to retrieve the _*optimal*_ output, we set a variable `min_diff` to infinity. This will be explained in the next paragraph.

We thus approach this problem in a case-by-case analysis. Let `sum_prices` be the sum of our "left" item's price and our "right" item's price. In technical terms, we set `sum_prices = prices[left] + prices[right]`, and our balance `b`. We enter one of the three following cases until our two pointers meet:

- Case 1: `sum_prices < b`. We would have some balance leftover if we were to purchase the items pointed by `left` and `right`. However, we are not so sure if this is our _*best*_ option. Let our variable `leftover` be `b - sum_prices`. Recall that we have the variable `min_diff`. The smaller the difference, the more we used up of our gift card. This is our ideal situation, so we check if `leftover < min_diff`. If so, then we have a currently optimal combination of gifts.
- Case 2: `sum_prices == b`. We can immediately end our algorithm in this scenario; we have fully maximized our gift card balance with the current left and right items. This is what we should get for our two friends with the gift card.
- Case 3: `sum_prices > b`. Decrement the right pointer by one. In the next iteration, `sum_prices` may decrease as a result of the sorted property in `prices`.

By the time the while loop ends (the two points meet), we would have had our optimal combination of gifts (or no combination).

### Analysis

Our algorithm, entitled `find_gifts` in the python code, contains one `while` loop such that it ends only if case 2 is reached or if the two pointers meet. Given that `left` increments by 1, and `right` decrements by 1, our pointers will eventually meet. In the worst-case scenario, our `left` pointer iterates through the entire array forwards, or vice versa for our `right` pointer. The operations that are ran during this iteration all are ran in O(1) time, since they are simply math operations (comparisons, addition/subtraction). `find_gifts` is therefore a linear scan through `prices`, so our total runtime is O(n).

The algorithm's proof of correctedness is mainly discussed in the previous section--but in short, it has to do with the sorted property that `prices` contains by assumption. This allows our two-pointer implementation to make small adjustments towards maximizing the gift card balance, whether we increase or decrease `sum_prices` in the next iteration. 

### Possible Extensions

1. If we were to pick 3 gifts for 3 friends, we can adjust the algorithm by perhaps iterating through the `prices` array from index `0` to `len(prices) - 2` and running `find_gifts` on the entire list (without the current item `prices[i]` and the balance `b - prices[i]`). We add the result of `find_gifts` and `prices[i]` together. By the end of this algorithm, we should have the most optimal set of 3 gifts. The use of complements in this algorithm and adjusting for the 3-gift solution would thus increase our runtime from linear to quadratic in the worst-case scenario.
2. If we were not hypothetically able to load the file into memory, what we can do instead is use buffers in order to load parts of the file at a time while performing the same algorithm (with two pointers `left` and `right`, of course). Implementing this would be especially more difficult due to having to keep track of byte offsets as parts of the file get loaded into the buffers.