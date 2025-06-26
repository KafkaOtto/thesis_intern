import numpy as np

import pandas as pd
from read_to_df import load_to_df
from scipy.stats import shapiro, ttest_rel

def compute_cohens_d(control_values, treatment_values):
    diff = np.array(control_values) - np.array(treatment_values)
    mean_diff = np.mean(diff)
    pooled_std = np.std(diff, ddof=1)
    small_constant = 1e-8  # Small constant to prevent division by zero
    cohens_d = mean_diff / (pooled_std + small_constant)
    return cohens_d

def perform_paired_ttests_with_effect_size(df, column, label, one_tailed=False):
    p_values = []
    keys = []
    test_results = []
    print("column: ", column)

    control_values = df[(df["treatment"] == "t1") & (df["variable"] == 'threshold0.58')][column].dropna().to_numpy()
    if control_values.size == 0:
        print("No control values found!")
        return

    grouped = df.groupby(["treatment", "variable"])[column]
    for (treatment, variable), values in grouped:
        if treatment == "t1" and variable == 'threshold0.58':
            continue

        if len(values) != len(control_values):
            print(f"Unmatched values!: {treatment}, {variable}, {column}" )
            longer, shorter = (
                (values, control_values)
                if len(values) > len(control_values)
                else (control_values, values)
            )
            difference = len(longer) - len(shorter)
            mean_value = np.mean(shorter)
            shorter = np.concatenate([shorter, [mean_value] * difference])
            if len(values) > len(control_values):
                control_values = shorter
            else:
                values = shorter
        # Perform the t-test
        if one_tailed:
            t_stat, p_value = ttest_rel(
                control_values, values, alternative="greater"
            )
        else:
            t_stat, p_value = ttest_rel(control_values, values)

        cohens_d = compute_cohens_d(control_values, values)
        significance = (
            "significantly different"
            if p_value < 0.05
            else "not significantly different"
        )
        test_results.append(
            f"Paired t-test for {label} {treatment}-{variable} vs control-{variable}: t-stat = {t_stat:.5f}, p-value = {p_value:.5f}, Cohen's d = {cohens_d:.5f} - Groups are {significance}"
        )
        p_values.append(p_value)
        keys.append(f"{treatment}-{variable}")

    corrected_p_values = holm_bonferroni_correction(p_values)

    for i, key in enumerate(keys):
        significance = (
            "significantly different"
            if corrected_p_values[i] < 0.05
            else "not significantly different"
        )
        print(
            test_results[i].replace(
                "Groups are",
                f"Corrected p-value = {corrected_p_values[i]:.5f} - Groups are",
            )
        )
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
    "t1": ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"],
    "t2": ["emb_768", "emb_384"],
    # "t3": ["deepseek_llama"],
    "t4": ["hnsw", "ivfflat"],
    "t5": ["caching_prefix"]
}

base_dir = "/Users/zhinuanguo/Downloads/rag_llmperf-add_rag/src/output_with_ram"

df = load_to_df(base_dir)
print(df.to_markdown())
perform_paired_ttests_with_effect_size(df, column="energy consumption", label="energy", one_tailed=True)
# perform_paired_ttests_with_effect_size(df, column="accuracy", label="accuracy(%)", one_tailed=True)
perform_paired_ttests_with_effect_size(df, column="latency", label="latency(ms)", one_tailed=True)