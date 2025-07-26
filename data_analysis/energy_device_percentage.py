import numpy as np

import pandas as pd
from helpers.read_to_df import load_to_df
from helpers.load_plots import plot_gpu_percentage
from helpers.utils import LABEL_MAPPING, TREATMENT_MAPPING

def perform_plots(df, group_orders):
    treatment_labels = []
    variable_labels = []
    energy_total_means = []
    energy_gpu_means = []


    grouped_energy_total = df.groupby(["treatment", "variable"])["energy_total"]
    grouped_energy_gpu = df.groupby(["treatment", "variable"])["energy_gpu"]

    for group in group_orders:
        for group_t, group_vs in group.items():
            for group_v in group_vs:
                energy_total_values = grouped_energy_total.get_group((group_t, group_v))
                energy_gpu_values = grouped_energy_gpu.get_group((group_t, group_v))
                if energy_total_values.size == 0:
                    continue
                if energy_gpu_values.size == 0:
                    continue
                treatment_labels.append(TREATMENT_MAPPING.get(group_t, group_t))
                variable_labels.append(LABEL_MAPPING.get(group_v, group_v))

                energy_total_means.append(np.mean(energy_total_values)/ 1000)
                energy_gpu_means.append(np.mean(energy_gpu_values) / 1000)
    plot_gpu_percentage(energy_gpu_means, energy_total_means, treatment_labels, variable_labels)

group_orders = [
    {"t1" : ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"]},
    {"t2": ["reranking_bm25s"]},
    {"t3": ["embedding_768", "embedding_384"]},
    {"t4": ["indexing_ivfflat", "indexing_hnsw"]},
    {"t6": ["caching_prefix"]},
    {"t7": ["combination_emb384with078"]},
]

base_dir = "../results/output_with_ram"

df = load_to_df(base_dir)

print(df.to_markdown())
perform_plots(df, group_orders)