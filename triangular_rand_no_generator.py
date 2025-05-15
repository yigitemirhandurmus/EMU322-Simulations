import numpy as np
import matplotlib.pyplot as plt
import time

np.random.seed(4521)  # Set seed for reproducibility

def triangular_pdf(x, a, c, b):
    """
    PDF of the triangular distribution with parameters:
    a = minimum value
    c = most likely value (mode)
    b = maximum value
    """
    if x < a or x > b:
        return 0
    elif a <= x <= c:
        return 2 * (x - a) / ((b - a) * (c - a))
    else:  # c < x <= b
        return 2 * (b - x) / ((b - a) * (b - c))

def theoretical_acceptance_probability(a, c, b):
    """
    Calculate the theoretical acceptance probability for the acceptance-rejection method
    on a triangular distribution with parameters a, c, b.
    
    The acceptance probability equals the ratio of the area under the PDF to 
    the area of the enclosing rectangle.
    """
    # Maximum height of the PDF (at mode c)
    max_pdf = triangular_pdf(c, a, c, b)
    
    # Area under the PDF is always 1 for a proper PDF
    pdf_area = 1.0
    
    # Area of the enclosing rectangle: width * height
    rectangle_area = (b - a) * max_pdf
    
    # Acceptance probability is the ratio
    acceptance_prob = pdf_area / rectangle_area
    
    return acceptance_prob

def acceptance_rejection_triangular(a, c, b, n):
    """
    Generate n random variates from a triangular distribution using acceptance-rejection method
    """
    # Find the maximum value of the PDF to set up the envelope
    # For triangular distribution, maximum is at the mode c
    max_pdf = triangular_pdf(c, a, c, b)
    
    # Initialize list to store generated values
    samples = []
    
    # Counter for accepted samples and total attempts
    accepted = 0
    attempts = 0
    
    # Continue until we have n samples
    while accepted < n:
        # Generate a uniform random number between a and b
        x = np.random.uniform(a, b)
        
        # Generate another uniform random number between 0 and max_pdf
        u = np.random.uniform(0, max_pdf)
        
        # Check if we accept this sample
        if u <= triangular_pdf(x, a, c, b):
            samples.append(x)
            accepted += 1
        
        attempts += 1
    
    acceptance_rate = accepted / attempts
    return np.array(samples), acceptance_rate

# Parameters for the triangular distribution
a = 10  # minimum
c = 30  # most likely
b = 40  # maximum
n = 500  # number of samples to generate

# Calculate theoretical acceptance probability
theoretical_prob = theoretical_acceptance_probability(a, c, b)

# Measure execution time
start_time = time.time()

# Generate the random variates
samples, empirical_prob = acceptance_rejection_triangular(a, c, b, n)
execution_time = time.time() - start_time

# Print statistics
print(f"Generated {n} triangular random variates")
print(f"Parameters: min={a}, mode={c}, max={b}")
print(f"Empirical acceptance rate: {empirical_prob:.4f}")
print(f"Theoretical acceptance probability: {theoretical_prob:.4f}")
print(f"Ratio (empirical/theoretical): {empirical_prob/theoretical_prob:.4f}")
print(f"Execution time: {execution_time:.4f} seconds")
print(f"Sample mean: {np.mean(samples):.4f}")
print(f"Sample variance: {np.var(samples, ddof=1):.4f}")
print(f"Theoretical mean: {(a + b + c)/3:.4f}")
print(f"Theoretical variance: {(a**2 + b**2 + c**2 - a*b - a*c - b*c)/18:.4f}")
emp_var = np.var(samples, ddof=1)
th_var = (a**2 + b**2 + c**2 - a*b - a*c - b*c) / 18
print(f"Variance error: {emp_var - th_var:.4g}")
print(f"Variance error (%): {(emp_var/th_var - 1)*100:.2f}%")


# Visualize the results
plt.figure(figsize=(12, 8))

# Plot 1: Histogram of generated samples
plt.subplot(2, 2, 1)
plt.hist(samples, bins=30, density=True, alpha=0.7, color='skyblue')
plt.title('Histogram of Generated Triangular Random Variates')
plt.xlabel('Value')
plt.ylabel('Density')

# Plot theoretical PDF for comparison
x = np.linspace(a, b, 1000)
y = [triangular_pdf(val, a, c, b) for val in x]
plt.plot(x, y, 'r-', lw=2, label='Theoretical PDF')
plt.legend()

# Plot 2: Visualization of acceptance-rejection method
plt.subplot(2, 2, 2)
# Create a dense grid of x values for plotting
x_grid = np.linspace(a, b, 1000)
y_pdf = np.array([triangular_pdf(x, a, c, b) for x in x_grid])
max_pdf = triangular_pdf(c, a, c, b)

# Plot PDF
plt.plot(x_grid, y_pdf, 'b-', lw=2, label='PDF')
# Plot envelope (rectangle)
plt.plot([a, a, b, b, a], [0, max_pdf, max_pdf, 0, 0], 'r--', lw=1.5, label='Envelope')
# Fill the area under the PDF
plt.fill_between(x_grid, y_pdf, alpha=0.3, color='blue', label='Acceptance Region')
# Fill the rejection region
plt.fill_between(x_grid, y_pdf, max_pdf, where=(y_pdf < max_pdf), alpha=0.3, color='red', label='Rejection Region')

plt.title('Acceptance-Rejection Method Visualization')
plt.xlabel('x')
plt.ylabel('Density')
plt.legend()

# Plot 3: Acceptance rate convergence
plt.subplot(2, 2, 3)
# Run a small simulation to show convergence of acceptance rate
acceptance_rates = []
sample_sizes = [10, 50, 100, 200, 300, 400, 500, 750, 1000]
for size in sample_sizes:
    _, rate = acceptance_rejection_triangular(a, c, b, size)
    acceptance_rates.append(rate)

plt.plot(sample_sizes, acceptance_rates, 'bo-', label='Empirical Rate')
plt.axhline(y=theoretical_prob, color='r', linestyle='--', label=f'Theoretical: {theoretical_prob:.4f}')
plt.title('Acceptance Rate Convergence')
plt.xlabel('Sample Size')
plt.ylabel('Acceptance Rate')
plt.legend()

plt.tight_layout()
plt.show()