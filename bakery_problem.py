import random
import numpy as np

# Constants
bagelPrice = 1.4  # Regular selling price per bagel
discountPrice = 0.7  # Half-price for unsold bagels
productionCost = 5.4 / 6  # Cost to make one bagel

# Generate required lists
bagelCustsProb = []
bagelCusts = []
bagelsSold = []
totalRevenue = []

# Possible values to test
bake_options = [216, 228, 240, 252, 264, 276, 288, 300]
results = {}

# Function to simulate one day
def simulate_day(num_to_bake):
    # Generate customer count
    prob1 = random.random()
    
    if 0 <= prob1 <= 0.20:
        customer_count = 10
    elif 0.20 < prob1 <= 0.30:
        customer_count = 12
    elif 0.30 < prob1 <= 0.60:
        customer_count = 14
    elif 0.60 < prob1 <= 0.85:
        customer_count = 16
    else:  # 0.85 < prob1 <= 1
        customer_count = 18
        
    # Determine bagels ordered by each customer
    total_ordered = 0
    for _ in range(customer_count):
        prob2 = random.random()
        
        if 0 <= prob2 <= 0.30:
            bagels_ordered = 12
        elif 0.30 < prob2 <= 0.70:  # 0.30 + 0.40
            bagels_ordered = 24
        elif 0.70 < prob2 <= 0.95:  # 0.70 + 0.25
            bagels_ordered = 36
        else:  # 0.95 < prob2 <= 1
            bagels_ordered = 48
            
        total_ordered += bagels_ordered
    
    # Calculate sales and revenue
    bagels_sold = min(total_ordered, num_to_bake)  # Can't sell more than we baked
    unsold_bagels = num_to_bake - bagels_sold
    
    # Calculate revenue
    revenue = (bagels_sold * bagelPrice) + (unsold_bagels * discountPrice)
    cost = num_to_bake * productionCost
    profit = revenue - cost
    
    return {
        'customers': customer_count,
        'ordered': total_ordered,
        'sold': bagels_sold,
        'unsold': unsold_bagels,
        'revenue': revenue,
        'cost': cost,
        'profit': profit
    }

# Run simulation for each baking option
for num_to_bake in bake_options:
    daily_profits = []
    daily_results = []
    
    # Run 500 simulations for each option
    for _ in range(500):
        day_result = simulate_day(num_to_bake)
        daily_profits.append(day_result['profit'])
        daily_results.append(day_result)
    
    # Store results
    results[num_to_bake] = {
        'avg_profit': np.mean(daily_profits),
        'std_profit': np.std(daily_profits),
        'total_profit': sum(daily_profits),
        'avg_unsold': np.mean([r['unsold'] for r in daily_results]),
        'avg_ordered': np.mean([r['ordered'] for r in daily_results]),
        'lost_sales_pct': np.mean([1 if r['ordered'] > r['sold'] else 0 for r in daily_results]) * 100
    }

# Print results table
print("\nSimulation Results (500 days each):\n")
print(f"{'Bagels':>6} | {'Avg Profit':>10} | {'Total Profit':>12} | {'Unsold Avg':>10} | {'Lost Sales %':>11}")
print("-" * 65)

for num in bake_options:
    r = results[num]
    print(f"{num:6d} | {r['avg_profit']:10.2f} | {r['total_profit']:12.2f} | {r['avg_unsold']:10.2f} | {r['lost_sales_pct']:11.2f}")

# Find optimal number
optimal = max(results.items(), key=lambda x: x[1]['avg_profit'])
print(f"\nOptimal number of bagels to bake per day: {optimal[0]} (average daily profit: {optimal[1]['avg_profit']:.2f} TL)")

# "Lost Sales %" represents the percentage of days when the bakery couldn't fulfill all customer orders because they didn't bake enough bagels.
