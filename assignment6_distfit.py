import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('assignment6_CSV.csv')
data = df['Value'].values

# Initialize results storage
results = []

# Print data summary
print(f"Data summary: Min={data.min():.3f}, Max={data.max():.3f}, Mean={data.mean():.3f}, Median={np.median(data):.3f}, Std={data.std():.3f}\n")

# Define distributions to fit
distributions = [
    ('Uniform', stats.uniform, 2),
    ('Exponential', stats.expon, 2),
    ('Gamma', stats.gamma, 3),
    ('Weibull', stats.weibull_min, 3),
    ('Normal', stats.norm, 2)
]

# Fit each distribution and compute metrics
for name, dist, k in distributions:
    try:
        # Fit distribution to data
        params = dist.fit(data)
        fitted_dist = dist(*params)
        
        # Kolmogorov-Smirnov test
        D, _ = stats.kstest(data, fitted_dist.cdf)
        
        # Log-likelihood and AIC
        log_likelihood = np.sum(fitted_dist.logpdf(data))
        aic = 2 * k - 2 * log_likelihood
        
        results.append({
            'Distribution': name,
            'Parameters': params,
            'KS Statistic (D)': D,
            'AIC': aic,
            'Fitted_Dist': fitted_dist  # Store fitted object
        })
    except Exception as e:
        print(f"Error fitting {name}: {str(e)}")

# Create results DataFrame
results_df = pd.DataFrame(results)

# Sort by KS Statistic for best/worst identification
results_df_sorted_ks = results_df.sort_values('KS Statistic (D)')

# Display results
print("Fitting Results (sorted by KS statistic):")
print(results_df_sorted_ks[['Distribution', 'KS Statistic (D)', 'AIC']])
print("\nFitting Results (sorted by AIC):")
print(results_df.sort_values('AIC')[['Distribution', 'KS Statistic (D)', 'AIC']])

# Identify best and worst fits based on KS statistic
best_dist_row_ks = results_df_sorted_ks.iloc[0]
worst_dist_row_ks = results_df_sorted_ks.iloc[-1]

best_dist_ks_name = best_dist_row_ks['Distribution']
worst_dist_ks_name = worst_dist_row_ks['Distribution']

best_dist_ks_obj = best_dist_row_ks['Fitted_Dist']
worst_dist_ks_obj = worst_dist_row_ks['Fitted_Dist']

print(f"\nBest fitting distribution (by KS): {best_dist_ks_name}")
print(f"Worst fitting distribution (by KS): {worst_dist_ks_name}")

# Identify best and worst fits based on AIC
results_df_sorted_aic = results_df.sort_values('AIC')
best_dist_aic_name = results_df_sorted_aic.iloc[0]['Distribution']
worst_dist_aic_name = results_df_sorted_aic.iloc[-1]['Distribution']

print(f"\nBest fitting distribution (by AIC): {best_dist_aic_name}")
print(f"Worst fitting distribution (by AIC): {worst_dist_aic_name}")

# --- Chi-Square Goodness of Fit Test Function ---
def chi_square_test(data, dist_obj, dist_name, alpha=0.05, min_expected_freq=5):
    """
    Performs Chi-Square goodness of fit test.
    
    Parameters:
    - data: observed data
    - dist_obj: fitted distribution object
    - dist_name: name of the distribution
    - alpha: significance level (default 0.05)
    - min_expected_freq: minimum expected frequency per bin (default 5)
    
    Returns:
    - Dictionary with test results
    """
    n = len(data)
    
    # Initial number of bins using Sturges' rule as starting point
    initial_bins = int(np.ceil(np.log2(n) + 1))
    
    # Find appropriate number of bins ensuring minimum expected frequency
    for num_bins in range(initial_bins, max(5, initial_bins//3), -1):
        # Create bins with equal probability intervals
        bin_edges = dist_obj.ppf(np.linspace(0.001, 0.999, num_bins + 1))
        
        # Handle infinite values by using data range
        bin_edges[0] = min(bin_edges[0], data.min() - 1e-6)
        bin_edges[-1] = max(bin_edges[-1], data.max() + 1e-6)
        
        # Count observed frequencies
        observed_freq, _ = np.histogram(data, bins=bin_edges)
        
        # Calculate expected frequencies
        expected_freq = np.full(num_bins, n / num_bins)
        
        # Check if all expected frequencies meet minimum requirement
        if np.all(expected_freq >= min_expected_freq):
            break
    else:
        # If we can't find suitable bins, use minimum bins
        num_bins = max(5, initial_bins//3)
        bin_edges = dist_obj.ppf(np.linspace(0.001, 0.999, num_bins + 1))
        bin_edges[0] = min(bin_edges[0], data.min() - 1e-6)
        bin_edges[-1] = max(bin_edges[-1], data.max() + 1e-6)
        observed_freq, _ = np.histogram(data, bins=bin_edges)
        expected_freq = np.full(num_bins, n / num_bins)
    
    # Calculate Chi-Square statistic
    chi2_stat = np.sum((observed_freq - expected_freq)**2 / expected_freq)
    
    # Degrees of freedom = number of bins - 1 - number of estimated parameters
    # Get number of parameters from the distribution
    if hasattr(dist_obj, 'args'):
        num_params = len(dist_obj.args) + 2  # args + loc + scale parameters
    else:
        # Fallback: use the k value from distributions list
        param_counts = {'Uniform': 2, 'Exponential': 2, 'Gamma': 3, 'Weibull': 3, 'Normal': 2}
        num_params = param_counts.get(dist_name, 2)
    
    df = num_bins - 1 - num_params
    df = max(1, df)  # Ensure at least 1 degree of freedom
    
    # Calculate p-value
    p_value = 1 - stats.chi2.cdf(chi2_stat, df)
    
    # Critical value
    critical_value = stats.chi2.ppf(1 - alpha, df)
    
    # Decision
    reject_null = chi2_stat > critical_value
    
    return {
        'Distribution': dist_name,
        'Chi2_Statistic': chi2_stat,
        'Degrees_of_Freedom': df,
        'P_Value': p_value,
        'Critical_Value': critical_value,
        'Reject_Null': reject_null,
        'Alpha': alpha,
        'Num_Bins': num_bins,
        'Observed_Freq': observed_freq,
        'Expected_Freq': expected_freq,
        'Bin_Edges': bin_edges
    }

# --- Perform Chi-Square Tests ---
print("\n" + "="*60)
print("CHI-SQUARE GOODNESS OF FIT TESTS (α = 0.05)")
print("="*60)

# Test for best fitting distribution
best_chi2_result = chi_square_test(data, best_dist_ks_obj, best_dist_ks_name)

print(f"\nBest Distribution: {best_chi2_result['Distribution']}")
print(f"Chi-Square Statistic: {best_chi2_result['Chi2_Statistic']:.4f}")
print(f"Degrees of Freedom: {best_chi2_result['Degrees_of_Freedom']}")
print(f"P-Value: {best_chi2_result['P_Value']:.6f}")
print(f"Critical Value (α=0.05): {best_chi2_result['Critical_Value']:.4f}")
print(f"Number of Bins Used: {best_chi2_result['Num_Bins']}")

if best_chi2_result['Reject_Null']:
    print("Decision: REJECT H₀ - The data does NOT follow this distribution")
    print("Interpretation: At α=0.05, we have sufficient evidence to conclude that")
    print(f"               the data does not follow a {best_dist_ks_name} distribution.")
else:
    print("Decision: FAIL TO REJECT H₀ - The data follows this distribution")
    print("Interpretation: At α=0.05, we do not have sufficient evidence to conclude that")
    print(f"               the data does not follow a {best_dist_ks_name} distribution.")

# Test for worst fitting distribution
worst_chi2_result = chi_square_test(data, worst_dist_ks_obj, worst_dist_ks_name)

print(f"\nWorst Distribution: {worst_chi2_result['Distribution']}")
print(f"Chi-Square Statistic: {worst_chi2_result['Chi2_Statistic']:.4f}")
print(f"Degrees of Freedom: {worst_chi2_result['Degrees_of_Freedom']}")
print(f"P-Value: {worst_chi2_result['P_Value']:.6f}")
print(f"Critical Value (α=0.05): {worst_chi2_result['Critical_Value']:.4f}")
print(f"Number of Bins Used: {worst_chi2_result['Num_Bins']}")

if worst_chi2_result['Reject_Null']:
    print("Decision: REJECT H₀ - The data does NOT follow this distribution")
    print("Interpretation: At α=0.05, we have sufficient evidence to conclude that")
    print(f"               the data does not follow a {worst_dist_ks_name} distribution.")
else:
    print("Decision: FAIL TO REJECT H₀ - The data follows this distribution")
    print("Interpretation: At α=0.05, we do not have sufficient evidence to conclude that")
    print(f"               the data does not follow a {worst_dist_ks_name} distribution.")

# --- Statistical Summary ---
print(f"\n" + "="*60)
print("STATISTICAL SUMMARY")
print("="*60)
print(f"Sample Size: {len(data)}")
print(f"Significance Level: α = 0.05")
print(f"Test Type: Chi-Square Goodness of Fit")
print(f"Best Distribution (KS): {best_dist_ks_name} (D = {best_dist_row_ks['KS Statistic (D)']:.4f})")
print(f"Worst Distribution (KS): {worst_dist_ks_name} (D = {worst_dist_row_ks['KS Statistic (D)']:.4f})")

# --- Optional: Create histogram comparison plots ---
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot for best distribution
x_range = np.linspace(data.min(), data.max(), 1000)
axes[0].hist(data, bins=30, density=True, alpha=0.7, color='skyblue', label='Observed Data')
axes[0].plot(x_range, best_dist_ks_obj.pdf(x_range), 'r-', linewidth=2, 
             label=f'Fitted {best_dist_ks_name}')
axes[0].set_xlabel('Value')
axes[0].set_ylabel('Density')
axes[0].set_title(f'Best Fit: {best_dist_ks_name} Distribution\n(χ² = {best_chi2_result["Chi2_Statistic"]:.4f}, p = {best_chi2_result["P_Value"]:.4f})')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot for worst distribution
axes[1].hist(data, bins=30, density=True, alpha=0.7, color='lightcoral', label='Observed Data')
axes[1].plot(x_range, worst_dist_ks_obj.pdf(x_range), 'r-', linewidth=2, 
             label=f'Fitted {worst_dist_ks_name}')
axes[1].set_xlabel('Value')
axes[1].set_ylabel('Density')
axes[1].set_title(f'Worst Fit: {worst_dist_ks_name} Distribution\n(χ² = {worst_chi2_result["Chi2_Statistic"]:.4f}, p = {worst_chi2_result["P_Value"]:.4f})')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()