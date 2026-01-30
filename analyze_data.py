import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Data (Volume of CO2 after 10 mins)
data_10min = {
    0: [32.0, 30.5, 34.2, 32.7, 33.4],
    1: [24.0, 23.8, 25.2, 23.4, 24.1],
    2: [17.0, 17.6, 16.8, 16.3, 16.4],
    3: [10.5, 11.0, 9.8, 11.1, 10.2],
    4: [6.5, 6.4, 6.5, 6.1, 6.7]
}

data_5min = {
    0: [4.0, 3.9, 4.3, 4.1, 4.2],
    1: [3.2, 3.0, 3.8, 2.9, 3.1],
    2: [2.4, 2.7, 2.4, 2.1, 2.2],
    3: [1.6, 1.6, 1.4, 1.8, 1.4],
    4: [1.0, 0.8, 1.2, 0.8, 1.0]
}

def analyze_and_plot(data, time_label, filename):
    concentrations = list(data.keys())
    # Create lists of values for ANOVA
    groups = [data[c] for c in concentrations]
    
    # One-Way ANOVA
    f_stat, p_value = stats.f_oneway(*groups)
    
    means = []
    stds = []
    
    # Calculate stats for table/plot
    for c in concentrations:
        values = data[c]
        means.append(np.mean(values))
        stds.append(np.std(values, ddof=1))

    # Write results to file
    with open(f"anova_results_{filename}.txt", "w") as f:
        f.write(f"--- ANOVA Results for {time_label} ---\n")
        f.write(f"F-statistic: {f_stat:.4f}\n")
        f.write(f"P-value: {p_value:.4e}\n")
        f.write("Meaning: " + ("Significant difference between groups (Reject H0)" if p_value < 0.05 else "No significant difference (Fail to reject H0)") + "\n")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.errorbar(concentrations, means, yerr=stds, fmt='o', capsize=5, capthick=1, ecolor='red', color='blue', label='Mean CO2 Volume')
    
    # Trendline (Linear)
    z = np.polyfit(concentrations, means, 1)
    p = np.poly1d(z)
    plt.plot(concentrations, p(concentrations), "g--", alpha=0.5, label=f'Trendline (R²={np.corrcoef(concentrations, means)[0,1]**2:.4f})')

    plt.title(f'Effect of NaCl Concentration on Yeast Fermentation ({time_label})')
    plt.xlabel('NaCl Concentration (%, w/v)')
    plt.ylabel(f'Volume of CO2 Produced (cm³)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(concentrations)
    plt.legend()
    
    output_path = f"{filename}.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    analyze_and_plot(data_5min, "5 Minutes", "yeast_fermentation_5min")
    analyze_and_plot(data_10min, "10 Minutes", "yeast_fermentation_10min")
