import math

# Parameters
predicted_profit_per_year = 0.05 # 5%
broker_fees = 0.02 # 2%
investment_amount = 1000
investment_period = 12 # in months

# Variables
total_profit = 0
total_cost = 0

# Calculate the profit and cost for each period
for i in range(investment_period):
    profit = investment_amount * predicted_profit_per_year / 12
    cost = 2
    total_profit += profit
    total_cost += cost
    investment_amount += profit - cost

# Calculate the final return on investment
final_return = (investment_amount - total_cost) / (investment_amount - total_cost + total_profit)

# Print the results
print("Final amount:", investment_amount)
print("Total profit:", total_profit)
print("Total cost:", total_cost)
print("Final return on investment: {:.2f}%".format(final_return * 100))
