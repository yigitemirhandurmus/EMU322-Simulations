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

# --- P-P Plotting Function ---
def plot_pp(data, dist_obj, dist_name, ax):
    """Generates a P-P plot."""
    sorted_data = np.sort(data)
    
    # Calculate empirical probabilities (y-values)
    # Using (i-0.5)/n which is common for plotting positions
    empirical_probs = (np.arange(len(sorted_data)) + 0.5) / len(sorted_data)
    
    # Calculate theoretical probabilities (x-values) using the CDF of the fitted distribution
    theoretical_probs = dist_obj.cdf(sorted_data)
    
    ax.plot(theoretical_probs, empirical_probs, 'o', markersize=4, label='Data')
    ax.plot([0, 1], [0, 1], 'r--', label='Ideal fit') # Diagonal line
    
    ax.set_xlabel('Theoretical Probabilities (CDF of Fitted Distribution)')
    ax.set_ylabel('Empirical Probabilities')
    ax.set_title(f'P-P Plot for {dist_name} Distribution')
    ax.legend()
    ax.grid(True)
    # Ensure axes are square and limits are [0,1] for better interpretation
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_aspect('equal', adjustable='box')

# --- Generate P-P Plots ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# P-P Plot for the best distribution (by KS)
if best_dist_ks_obj:
    plot_pp(data, best_dist_ks_obj, best_dist_ks_name, axes[0])
else:
    axes[0].text(0.5, 0.5, f"Could not plot for {best_dist_ks_name}\n(no fitted object)", 
                 horizontalalignment='center', verticalalignment='center')
    axes[0].set_title(f'P-P Plot for {best_dist_ks_name} Distribution')

# P-P Plot for the worst distribution (by KS)
if worst_dist_ks_obj:
    plot_pp(data, worst_dist_ks_obj, worst_dist_ks_name, axes[1])
else:
    axes[1].text(0.5, 0.5, f"Could not plot for {worst_dist_ks_name}\n(no fitted object)", 
                 horizontalalignment='center', verticalalignment='center')
    axes[1].set_title(f'P-P Plot for {worst_dist_ks_name} Distribution')

plt.tight_layout()
plt.show()