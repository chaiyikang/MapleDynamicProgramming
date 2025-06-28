COST10 = 3
COST60 = 2.3
COST100 = 0.18


prices = [
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.9, 3, 5, 10, 20, 40, 120, 240, 480, 960, 2000],
    [0] * 16,
    [0] * 16,
    [0] * 16,
    [0] * 16,
    [0] * 16,
]


actions = [["" for _ in range(16)] for _ in range(6)]


def dp():
    memo = [[None for _ in range(16)] for _ in range(6)]

    def helper(slots, attack) -> int:
        # if slots < 0 or slots > 5 or attack < 0 or attack > 15:
        #     return 0
        if memo[slots][attack] is not None:
            return memo[slots][attack]
        if slots == 0:
            result = prices[slots][attack]
            memo[slots][attack] = result
            actions[slots][attack] = "Sell"
            return result
        sell = prices[slots][attack]
        ten = round(
            -COST10
            + 0.1 * helper(slots - 1, attack + 3)
            + 0.9 * helper(slots - 1, attack),
            1,
        )
        sixty = round(
            -COST60
            + 0.6 * helper(slots - 1, attack + 2)
            + 0.4 * helper(slots - 1, attack),
            1,
        )
        hundred = round(-COST100 + helper(slots - 1, attack + 1), 1)
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
