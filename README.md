# Dynamic Programming in Maplestory Artale

## Context

In MapleStory, equipment can be "scrolled" to make them stronger. However, there is a limit on the number of scrolls that can be used on a piece of equipment. Mainly 3 types of scrolls exist, 10%(+3), 60%(+2) and 100%(+1) scrolls. If the scrolling fails, the scrolling limit on the equipment is still consumed without stats being added to the equipment. In return, lower probability scrolls add more stats.

Equipment are sold on an auction house. There are two types of state for a piece of equipment. The added stats, and the number of scrolling slots left. There is a positive relationship between each of these states and the market valuation for the equipment. More slots left represents higher maximum potential stat for the equipment, hence are valued higher.

## Goal

An enterprising player might consider buying equipment and scrolls, scrolling the equipment and selling it for a profit. Assuming the market valuations for the different possible combinations of stats and slots left are available, how can one determine if such a process is profitable? If it is profitable, how do we determine the best possible strategy for scrolling?

## Initial Intuition

Initially, I though the best "strategy" constitued a specific sequence of scrolls, such that the expected payoff is maximised. However, the one might intuit that the best strategy would optimise differently based on the result of each step of scrolling. So ideally, we want to know, for every possible outcome of scrolling, what the next best step is that maximises the expected profit.

## Dynamic Programming

This problem felt extremely complicated and seemed like it would involve a lot of complicated calculations of expectation. However, by the magic of dynamic programming, it turns out this problem is very easily solved.

Essentially, for every state, there are 4 possible decisions. To scroll with 100%, 60%, 10% (but incurring the cost of purchasing the scroll), or to sell the equipment as it is and cash out.

### Recurrence Relation

```python
dp[stat, slots] = max(
    price[stat][slots], # cash out
    -COST10 + 0.1 * dp[stat + 3, slots - 1] + 0.9 * dp[stat, slots - 1], # buy and use a 10% scroll
    -COST60 + 0.6 * dp[stat + 2, slots - 1] + 0.4 * dp[stat, slots - 1]
    -COST100 + dp[stat + 1, slots - 1]
)
```

The base case is when slots = 0, where the only option is to sell the equipment.

## Algorithm

```python
actions = [["" for _ in range(16)] for _ in range(6)]

def dp():
    memo = [[None for _ in range(16)] for _ in range(6)]

    def helper(slots, attack) -> int:
        if slots < 0 or slots > 5 or attack < 0 or attack > 15:
            return float('-inf')
        if memo[slots][attack] is not None:
            return memo[slots][attack]
        if slots == 0:
            result = prices[slots][attack]
            memo[slots][attack] = result
            actions[slots][attack] = "Sell"
            return result
        sell = prices[slots][attack]
        ten = -COST10 + 0.1 * helper(slots - 1, attack + 3) + 0.9 * helper(slots - 1, attack)
        sixty = -COST60 + 0.6 * helper(slots - 1, attack + 2) + 0.4 * helper(slots - 1, attack)
        hundred = -COST100 + helper(slots - 1, attack + 1)
        result = max(sell, ten, sixty, hundred)
        memo[slots][attack] = result
        if result == sell:
            actions[slots][attack] = "Sell"
        elif result == ten:
            actions[slots][attack] = "use 10%"
        elif result == sixty:
            actions[slots][attack] = "use 60%"
        elif result == hundred:
            actions[slots][attack] = "use 100%"
        # print()
        # print(actions)
        return result

    clean = helper(5, 0)
    print(memo)
    return clean


print(dp())
# dp()
print(actions)
```

## Implication

This implementation was written for gloves with 5 scrolling slot and therefore a theoretical maximum of 15 attack.
We make sure to record what the best option is at each state.
The values in the memoization table essentially tell us, for each state, the maximum expected profit we can make, ignoring the cost to get the current glove but internalising the cost of scrolls. So if we look at the value in the table corresponding to 5 slots left and 0 attack, it tells us how much we can profit if we start from a clean unscrolled pair of gloves.
This is useful because we don't necessarily have to start our enterprise from clean gloves, we can buy partially scrolled gloves from the market as well. In such cases, we compare the price of the glove to the expected profit in the table and determine if it is profitable.
