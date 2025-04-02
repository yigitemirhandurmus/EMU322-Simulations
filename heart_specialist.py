import random
import numpy as np

def simulate_heart_specialist():
    # Constants
    patients_per_day = 16
    service_time_scheduled = 30  # minutes
    start_time = 9 * 60  # 9 AM in minutes from midnight
    simulation_days = 200
    
    # Arrival time distribution (in minutes relative to scheduled time)
    arrival_times = [-15, -5, 0, 10, 15]
    arrival_probabilities = [0.10, 0.25, 0.50, 0.10, 0.05]
    
    # Service time distribution (in minutes)
    service_times = [24, 27, 30, 33, 36, 39]
    service_probabilities = [0.20, 0.25, 0.30, 0.10, 0.10, 0.05]
    
    # Statistics tracking
    total_patients = patients_per_day * simulation_days
    patients_not_waiting = 0
    last_patients_not_waiting = 0
    doctor_busy_time = 0
    total_simulation_time = 0
    
    # Run simulation for specified number of days
    for day in range(simulation_days):
        # Reset doctor's state for the day
        current_time = start_time
        doctor_free_time = start_time
        
        # Process each patient for the day
        for patient in range(patients_per_day):
            # Calculate scheduled arrival time
            scheduled_time = start_time + patient * service_time_scheduled
            
            # Determine actual arrival time (apply offset based on distribution)
            arrival_offset = np.random.choice(arrival_times, p=arrival_probabilities)
            actual_arrival = scheduled_time + arrival_offset
            
            # Determine service duration for this patient
            service_duration = np.random.choice(service_times, p=service_probabilities)
            
            # Calculate when patient can start being served
            start_service_time = max(actual_arrival, doctor_free_time)
            
            # Check if patient had to wait
            if start_service_time <= actual_arrival:
                patients_not_waiting += 1
                
            # Check if this is the last patient of the day
            if patient == patients_per_day - 1 and start_service_time <= actual_arrival:
                last_patients_not_waiting += 1
            
            # Update doctor's free time
            doctor_free_time = start_service_time + service_duration
            
            # Track doctor's busy time
            doctor_busy_time += service_duration
        
        # Track total simulation time (from start to when doctor finishes with last patient)
        total_simulation_time += (doctor_free_time - start_time)
    
    # Calculate performance measures
    prob_patient_not_wait = patients_not_waiting / total_patients
    prob_last_patient_not_wait = last_patients_not_waiting / simulation_days
    doctor_utilization = doctor_busy_time / total_simulation_time
    
    return {
        "probability_patient_not_wait": prob_patient_not_wait,
        "probability_last_patient_not_wait": prob_last_patient_not_wait,
        "doctor_utilization": doctor_utilization
    }

# Run the simulation and print results
if __name__ == "__main__":
    np.random.seed(1)  # Set seed for reproducibility
    random.seed(1)
    
    results = simulate_heart_specialist()
    
    print("Heart Specialist Clinic Simulation Results (200 days):")
    print(f"a. Probability that a patient will not wait: {results['probability_patient_not_wait']:.4f}")
    print(f"b. Probability that the last patient will not wait: {results['probability_last_patient_not_wait']:.4f}")
    print(f"c. Utilization of the specialist: {results['doctor_utilization']:.4f}")
    