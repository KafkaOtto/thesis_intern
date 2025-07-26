import numpy as np

import pandas as pd
from helpers.read_to_df import load_to_df
from scipy.stats import shapiro, ttest_rel
from helpers.utils import LABEL_MAPPING, TREATMENT_MAPPING, RED, RESET, group_orders_combo
from helpers.load_plots import plot_metrics_comparison

def compute_cohens_d(control_values, treatment_values):
    diff = np.array(control_values) - np.array(treatment_values)
    mean_diff = np.mean(diff)
    pooled_std = np.std(diff, ddof=1)
    small_constant = 1e-8  # Small constant to prevent division by zero
    cohens_d = mean_diff / (pooled_std + small_constant)
    return cohens_d

def perform_paired_ttests_with_effect_size(df, group, column, label, one_tailed=False):
    p_values = []
    treatment_labels = []
    variable_labels = []
    test_results = []
    effect_sizes = []
    percentage_changes = []

    print("column: ", column)

    control_values = df[(df["treatment"] == "t1") & (df["variable"] == 'thresholds_base0.58')][column].dropna().to_numpy()
    print(f"control mean values: {np.mean(control_values)} for column: {column}")
    if control_values.size == 0:
        print("No control values found!")
        return

    grouped = df.groupby(["treatment", "variable"])[column]

    for item_group in group_orders_combo:
        for group_t, group_vs in item_group.items():
            for group_v in group_vs:
                values = grouped.get_group((group_t, group_v))
                if values.size == 0:
                    continue
                control_values = control_values.astype(np.float64)
                values = values.astype(np.float64)
                if len(values) != len(control_values):
                    print(f"{RED}Unmatched values!: {label} {group_t}-{group_v}{RESET}")
                    return
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
                    f"Paired t-test for {label} {group_t}-{group_v} vs control-threshold0.58: t-stat = {t_stat:.5f}, p-value = {p_value:.5f}, Cohen's d = {cohens_d:.5f} - Groups are {significance}"
                )
                effect_sizes.append(cohens_d)
                p_values.append(p_value)
                # treatment_labels.append(TREATMENT_MAPPING.get(group_t, group_t))
                # variable_labels.append(LABEL_MAPPING.get(group_v, group_v))

                control_mean = np.mean(control_values)
                val_mean = np.mean(values)
                percentage_decrease = ((val_mean - control_mean) / control_mean) * 100
                if 'accuracy' in column:
                    percentage_changes.append(percentage_decrease)
                else:
                    percentage_changes.append(-percentage_decrease)

    corrected_p_values = holm_bonferroni_correction(p_values)

    i = 0
    result_percentage_changes = []

    for item_group in group_orders_combo:
        for group_t, group_vs in item_group.items():
            for group_v in group_vs:
                if group_t == group:
                    treatment_labels.append(TREATMENT_MAPPING.get(group_t, group_t))
                    variable_labels.append(LABEL_MAPPING.get(group_v, group_v))
                    if corrected_p_values[i] < 0.05:
                        result_percentage_changes.append(percentage_changes[i])
                    else:
                        result_percentage_changes.append(0.0)
                i += 1

    return treatment_labels, variable_labels, result_percentage_changes



def holm_bonferroni_correction(p_values):
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p_values = np.array(p_values)[sorted_indices]
    corrected_p_values = np.empty(n)

    for i in range(n):
        corrected_p_values[sorted_indices[i]] = min(1, sorted_p_values[i] * (n - i))

    return corrected_p_values

metrics = ["energy", "responses", "accuracies"]

base_dir = "../results/output_with_ram"

df = load_to_df(base_dir)

for group in group_orders_combo:
    group_k = list(group.keys())[0]
    treatment_labels, variable_labels, energy_percentage_changes = perform_paired_ttests_with_effect_size(df, group=group_k, column="energy_total", label="energy(J)", one_tailed=True)
    treatment_labels, variable_labels, accuracy_percentage_changes = perform_paired_ttests_with_effect_size(df, group=group_k, column="accuracy", label="accuracy(%)", one_tailed=False)
    treatment_labels, variable_labels, latency_percentage_changes = perform_paired_ttests_with_effect_size(df, group=group_k, column="latency", label="latency(ms)", one_tailed=False)

    # For energy vs latency comparison
    # plot_metrics_comparison(
    #     metrics_data={'energy reduction': energy_percentage_changes, 'latency decrease': latency_percentage_changes},
    #     treatment_labels=treatment_labels,
    #     variable_labels=variable_labels,
    #     title="Energy vs Latency Comparison",
    #     save_path=f"plots/energy_latency_comparison_{group_k}.png"
    # )

    # For all three metrics comparison
    plot_metrics_comparison(
        metrics_data={'energy reduction': energy_percentage_changes, 'latency reduction': latency_percentage_changes, 'accuracy changes': accuracy_percentage_changes},
        treatment_labels=treatment_labels,
        variable_labels=variable_labels,
        title="Energy, Latency and Accuracy Comparison",
        save_path=f"plots/all_metrics_comparison_{group_k}.pdf"
    )