import pandas as pd
import os


def write_to_excel_and_open(matrix, filename="output.xlsx"):
    # Convert the 2D list into a DataFrame
    df = pd.DataFrame(matrix)

    # Write to Excel
    df.to_excel(filename, index=False, header=False)

    # Open the file (Windows)
    os.startfile(filename)


def maple(
    scrollCosts: list[float], scrollStats: list[int], prices: list[float], slots: int
):
    maxStat = len(prices)
    actions = [["" for _ in range(maxStat + 1)] for _ in range(slots + 1)]
    memo = [[None for _ in range(maxStat + 1)] for _ in range(slots + 1)]
    COST10, COST60, COST100 = scrollCosts
    STAT10, STAT60, STAT100 = scrollStats

    def helper(slots, stat):
        if memo[slots][stat] is not None:
            return memo[slots][stat]
        if slots == 0:
            result = prices[stat]
            memo[slots][stat] = result
            actions[slots][stat] = "Sell"
            return result
        sell = 0 if slots > 0 else prices[stat]
        ten = round(
            -COST10
            + 0.1 * helper(slots - 1, stat + STAT10)
            + 0.9 * helper(slots - 1, stat),
            1,
        )
        sixty = round(
            -COST60
            + 0.6 * helper(slots - 1, stat + STAT60)
            + 0.4 * helper(slots - 1, stat),
            1,
        )
        hundred = round(-COST100 + helper(slots - 1, stat + STAT100), 1)

        result = max(sell, ten, sixty, hundred)
        memo[slots][stat] = result
        if result == sell:
            actions[slots][stat] = "Sell"
        elif result == ten:
            actions[slots][stat] = "use 10%"
        elif result == sixty:
            actions[slots][stat] = "use 60%"
        elif result == hundred:
            actions[slots][stat] = "use 100%"
        return result

    res = helper(slots, 0)
    print(f"expected profit from clean: {res}")

    write_to_excel_and_open(actions)
    print()
    write_to_excel_and_open(memo)
