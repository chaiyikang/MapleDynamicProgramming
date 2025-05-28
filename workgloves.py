COST10 = 1
COST60 = 2
COST100 = 0.5
prices = [
    # 0 slots remaining - Real data at indices: [3]=0.68, [4]=1.00, [5]=2.63, [6]=5.96, [8]=19.50, [9]=26.00, [10]=40.00
    [0.00, 0.20, 0.40, 0.68, 1.00, 2.63, 5.96, 12.0, 19.50, 26.00, 40.00, 58.0, 82.0, 115.0, 160.0, 220.0],
    
    # 1 slot remaining - All unknown, estimate with slot premium
    [0.00, 0.30, 0.60, 1.02, 1.50, 3.95, 8.94, 18.0, 29.25, 39.0, 60.0, 87.0, 123.0, float('-inf'), float('-inf'), float('-inf')],
    
    # 2 slots remaining - Real data: [4]=3.70
    [0.00, 0.40, 0.80, 1.36, 3.70, 5.26, 11.92, 24.0, 39.0, 52.0, float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf')],
    
    # 3 slots remaining - Real data: [2]=1.00
    [0.00, 0.60, 1.00, 2.04, 5.55, 7.89, 17.88, float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf')],
    
    # 4 slots remaining - Real data: [3]=8
    [0.00, 1.20, 2.00, 8.00, float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf')],
    
    # 5 slots remaining - Real data: [0]=0.10
    [0.10, float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf')]
]



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


