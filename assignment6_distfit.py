import numpy as np
import pandas as pd
import scipy.stats as stats

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
results_df = pd.DataFrame(results).sort_values('KS Statistic (D)')

# Display results
print("Fitting Results:")
print(results_df[['Distribution', 'KS Statistic (D)', 'AIC']])

# Identify best and worst fits
best_dist_ks = results_df.iloc[0]['Distribution']
worst_dist_ks = results_df.iloc[-1]['Distribution']

best_dist_aic = results_df.loc[results_df['AIC'].idxmin()]['Distribution']
worst_dist_aic = results_df.loc[results_df['AIC'].idxmax()]['Distribution']

print(f"\nBest fit (KS): {best_dist_ks}")
print(f"Worst fit (KS): {worst_dist_ks}")
print(f"\nBest fit (AIC): {best_dist_aic}")
print(f"Worst fit (AIC): {worst_dist_aic}")