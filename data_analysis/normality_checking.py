from scipy.stats import shapiro, zscore
import tabulate
import pandas as pd
from helpers.read_to_df import load_to_df
from helpers.utils import RED, GREEN, RESET

# Function to check normality using Shapiro-Wilk test
def check_normality(values, key, label):
    # Remove None or NaN values

    values = [v for v in values if v is not None and pd.notna(v)]

    if len(values) < 3:
        print(f"{label} Group {key}:  Not enough valid data for normality test.")
        return

    stat, p_value = shapiro(values)
    alpha = 0.05
    if p_value > alpha:
        print(f"{label} Group {key}: Normally distributed (p-value={p_value:.5f})")
    else:
        print(f"{RED}{label} Group {key}: Not normally distributed (p-value={p_value:.5f}){RESET}")
        for i in range(len(values)):
            reduced = values[:i] + values[i + 1:]
            if len(reduced) >= 3:
                stat, p = shapiro(reduced)
                print(
                        f"{GREEN}Normality after removing index {i}, value {values[i]:.5f} (p={p:.5f}){RESET}")

base_dir = "../results/output_with_ram"
df = load_to_df(base_dir)
print(df.to_markdown(floatfmt='.05f'))
grouped_energy = df.groupby(['treatment', 'variable'])['energy_total'].apply(list)
grouped_accuracy = df.groupby(['treatment', 'variable'])['accuracy'].apply(list)
grouped_latency = df.groupby(['treatment', 'variable'])['latency'].apply(list)
for key, values in grouped_energy.items():
    check_normality(values, key, label="Energy")

for key, values in grouped_latency.items():
    check_normality(values, key, label="Latency")

for key, values in grouped_accuracy.items():
    check_normality(values, key, label="Accuracy")
