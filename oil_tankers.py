import random

''' A and B terminals

B is more efficient than A therefore is preferred

'''

tankers_to_simulate = 10

# Define the number of days for unloading

supertanker_unload_days_A = 4
supertanker_unload_days_B = 3

midsize_unload_days_A = 3
midsize_unload_days_B = 2

small_unload_days_A = 2
small_unload_days_B = 1

# IAT (days) and Probabilities

tanker_data = {}

for i in range(0, tankers_to_simulate):
    prob1 = random.random()
    prob2 = random.random()

    # Determine IAT
    if 0 <= prob1 <= 0.30:
        iat = 2
    elif 0.30 < prob1 <= 0.50:
        iat = 3
    elif 0.50 < prob1 <= 0.60:
        iat = 4
    elif 0.60 < prob1 <= 0.75:
        iat = 5
    elif 0.75 < prob1 <= 1:
        iat = 6

    # Determine tanker size
    if 0 <= prob2 <= 0.20:
        tanker_size = "supertanker"
    elif 0.20 < prob2 <= 0.65:
        tanker_size = "midsize"
    elif 0.65 < prob2 <= 1:
        tanker_size = "small"

    # Add to dictionary
    tanker_data[i] = {iat: tanker_size}

print(tanker_data)