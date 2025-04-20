import random

''' A and B terminals

B is more efficient than A therefore is preferred

'''

tankers_to_simulate = 10

# Define the number of days for unloading by tanker size at each terminal
unload_times = {
    "supertanker": {"A": 4, "B": 3},
    "midsize": {"A": 3, "B": 2},
    "small": {"A": 2, "B": 1}
}

# Lists to hold tanker simulation events
# Each event is a dict with keys: arrival, start, departure, terminal
events = []

# Next available times for each terminal
next_free = {"A": 0, "B": 0}

# Current simulation time initialized to zero
current_time = 0

# Generate arrivals and assign terminals
for i in range(tankers_to_simulate):
    # Generate random numbers for interarrival time and tanker size selection
    prob1 = random.random()
    prob2 = random.random()

    # Determine interarrival time (IAT)
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

    # Update current time with interarrival time
    arrival_time = current_time + iat
    current_time = arrival_time

    # Determine tanker size
    if 0 <= prob2 <= 0.20:
        tanker_size = "supertanker"
    elif 0.20 < prob2 <= 0.65:
        tanker_size = "midsize"
    elif 0.65 < prob2 <= 1:
        tanker_size = "small"

    # Decide which terminal will process the tanker
    # Prefer terminal B when available at the time of arrival.
    if arrival_time >= next_free["B"]:
        terminal = "B"
        start_time = arrival_time
    elif arrival_time >= next_free["A"]:
        terminal = "A"
        start_time = arrival_time
    else:
        # Both terminals are busy.
        # Assign the tanker to whichever terminal becomes free sooner.
        if next_free["B"] <= next_free["A"]:
            terminal = "B"
            start_time = next_free["B"]
        else:
            terminal = "A"
            start_time = next_free["A"]

    # Determine unload duration based on tanker size and terminal
    duration = unload_times[tanker_size][terminal]
    departure_time = start_time + duration

    # Update terminal availability
    next_free[terminal] = departure_time

    # Record the event with tanker type information
    events.append({
        "arrival": arrival_time,
        "start": start_time,
        "departure": departure_time,
        "terminal": terminal,
        "tanker_size": tanker_size
    })

# Determine final simulation time (last departure)
sim_end = max(event["departure"] for event in events)

# Now, calculate the average occupancy at each terminal.
# We will simulate time changes at each event (arrival, start, departure)
# and compute occupancy as a piecewise constant function.
# We'll build a list of time points with changes in occupancy for each terminal.
time_changes = []
for event in events:
    # When a tanker starts unloading, it "enters" the terminal.
    time_changes.append((event["start"], event["terminal"], +1))
    # When it departs, it "leaves" the terminal.
    time_changes.append((event["departure"], event["terminal"], -1))

# Sort the time changes by time
time_changes.sort(key=lambda x: x[0])

# Occupancies
occupancy = {"A": 0, "B": 0}
# Total "occupancy-time" accumulated per terminal
total_occupancy_time = {"A": 0, "B": 0}
last_time = 0

for time_point, term, change in time_changes:
    # Calculate time elapsed since the last event
    dt = time_point - last_time
    # Accumulate occupancy-time for both terminals over dt
    for t in ["A", "B"]:
        total_occupancy_time[t] += occupancy[t] * dt
    # Update occupancy for the terminal with the event
    occupancy[term] += change
    last_time = time_point

# Calculate average occupancy = total occupancy-time divided by simulation end time
avg_A = total_occupancy_time["A"] / sim_end
avg_B = total_occupancy_time["B"] / sim_end

print("Tanker events:")
for event in events:
    print(event)

# Count the number of tankers processed at each terminal
num_tankers_A = sum(1 for event in events if event["terminal"] == "A")
num_tankers_B = sum(1 for event in events if event["terminal"] == "B")

print("\nNumber of tankers processed:")
print(f"Terminal A: {num_tankers_A}")
print(f"Terminal B: {num_tankers_B}")

print("\nUtilization:")
print(f"Terminal A: {avg_A:.2f}")
print(f"Terminal B: {avg_B:.2f}")

# Calculate the average number of days in port for each tanker type
total_days_in_port = {}
tanker_counts = {}

for event in events:
    tanker_type = event["tanker_size"]
    # The days in port equals departure time minus arrival time
    time_in_port = event["departure"] - event["arrival"]
    total_days_in_port[tanker_type] = total_days_in_port.get(tanker_type, 0) + time_in_port
    tanker_counts[tanker_type] = tanker_counts.get(tanker_type, 0) + 1

print("\nAverage days in port per tanker type:")
for tanker_type in total_days_in_port:
    avg_days = total_days_in_port[tanker_type] / tanker_counts[tanker_type]
    print(f"{tanker_type}: {avg_days:.0f}")