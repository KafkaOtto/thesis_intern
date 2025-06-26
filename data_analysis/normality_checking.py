from scipy.stats import shapiro, zscore
import tabulate
import pandas as pd
from read_to_df import load_to_df
from utils import RED, GREEN, RESET

# Function to check normality using Shapiro-Wilk test
def check_normality(values, key, label):
    # Remove None or NaN values

    values = [v for v in values if v is not None and pd.notna(v)]

    if len(values) < 3:
        print(f"{label} Group {key}:  Not enough valid data for normality test.")
        return
    if "embedding_384" in key:
        print("values", values)

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


# zs = zscore(values)
    # outliers = [(i, v, zs[i]) for i, v in enumerate(values) if abs(zs[i]) > 2]
    #
    # if outliers:
    #     print(f"{label} Group {key}    → {len(outliers)} potential outlier(s) based on Z-score (|z| > 2):")
    #     for idx, val, z in outliers:
    #         print(f"{label} Group {key}      - Index {idx}, Value: {val:.5f}, Z-score: {z:.2f}")
    # else:
    #     print(f"    → No strong outliers based on Z-score (|z| > 2)")

metrics = ["energy", "responses", "accuracies"]

treatments = {
    "t1": ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"],
    "t2": ["emb_768", "emb_384"],
    # "t3": ["deepseek_llama"],
    "t4": ["hnsw", "ivfflat"],
    "t5": ["caching_prefix"]
}

base_dir = "../results/output_with_ram"
df = load_to_df(base_dir)
print(df.to_markdown(floatfmt='.05f'))
grouped_energy = df.groupby(['treatment', 'variable'])['energy consumption'].apply(list)
grouped_accuracy = df.groupby(['treatment', 'variable'])['accuracy'].apply(list)
grouped_latency = df.groupby(['treatment', 'variable'])['latency'].apply(list)
for key, values in grouped_energy.items():
    check_normality(values, key, label="Energy")

for key, values in grouped_latency.items():
    check_normality(values, key, label="Latency")

for key, values in grouped_accuracy.items():
    check_normality(values, key, label="Accuracy")
