import numpy as np

import pandas as pd
from read_to_df import load_to_df
from scipy.stats import shapiro, ttest_rel
from scipy.stats import ttest_ind
from load_plots import plot_effect_sizes

def compute_cohens_d_unpaired(x, y):
    # For unpaired data (Cohen’s d for independent samples)
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / dof)
    return (np.mean(x) - np.mean(y)) / (pooled_std + 1e-8)

def perform_unpaired_ttests_with_effect_size(df, column, label, one_tailed=False):
    p_values = []
    keys = []
    test_results = []
    effect_sizes = []

    print("column: ", column)

    control_values = df[(df["treatment"] == "t1") & (df["variable"] == 'thresholds_base0.58')][column].dropna().to_numpy()
    if control_values.size == 0:
        print("No control values found!")
        return

    grouped = df.groupby(["treatment", "variable"])[column]
    for (treatment, variable), values in grouped:
        if treatment == "t1" and variable == 'threshold0.58':
            continue

        values = values.dropna().to_numpy()
        if values.size == 0:
            continue

        control_values = control_values.astype(np.float64)
        values = values.astype(np.float64)
        # Welch’s t-test
        t_stat, p_value = ttest_ind(control_values, values, equal_var=False, alternative="greater" if one_tailed else "two-sided")
        cohens_d = compute_cohens_d_unpaired(control_values, values)
        significance = "significantly different" if p_value < 0.05 else "not significantly different"
        test_results.append(
            f"Unpaired t-test for {label} {treatment}-{variable} vs control-threshold0.58: t-stat = {t_stat:.5f}, p-value = {p_value:.5f}, Cohen's d = {cohens_d:.5f} - Groups are {significance}"
        )
        effect_sizes.append(cohens_d)
        p_values.append(p_value)
        keys.append(f"{treatment}-{variable}")

    corrected_p_values = holm_bonferroni_correction(p_values)

    for i, key in enumerate(keys):
        significance = "significantly different" if corrected_p_values[i] < 0.05 else "not significantly different"
        print(test_results[i].replace("Groups are", f"Corrected p-value = {corrected_p_values[i]:.5f} - Groups are"))

    plot_effect_sizes(effect_sizes, keys, f"t-test for {label}", p_values)

def holm_bonferroni_correction(p_values):
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p_values = np.array(p_values)[sorted_indices]
    corrected_p_values = np.empty(n)

    for i in range(n):
        corrected_p_values[sorted_indices[i]] = min(1, sorted_p_values[i] * (n - i))

    return corrected_p_values


metrics = ["energy", "responses", "accuracies"]

treatments = {
    "t1_thresholds": ["base0.58", "0.68", "0.78", "0.88"],
    "t2_embedding": ["768", "384"],
    "t4_indexing": ["hnsw", "ivfflat"],
    "t5_caching": ["prefix"]
}

# treatments = {
#     "t1": ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"],
#     "t2": ["emb_768", "emb_384"],
#     # "t3": ["deepseek_llama"],
#     "t4": ["hnsw", "ivfflat"],
#     "t5": ["caching_prefix"]
# }

base_dir = "../results/output_with_ram"

df = load_to_df(base_dir)
print(df.to_markdown())
perform_unpaired_ttests_with_effect_size(df, column="energy consumption", label="energy", one_tailed=True)
perform_unpaired_ttests_with_effect_size(df, column="accuracy", label="accuracy(%)", one_tailed=True)
perform_unpaired_ttests_with_effect_size(df, column="latency", label="latency(ms)", one_tailed=True)