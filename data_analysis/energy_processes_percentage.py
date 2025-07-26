import numpy as np
import pandas as pd
from helpers.read_to_df import load_to_df
from helpers.load_plots import plot_energy_breakdown  # Updated import
from helpers.utils import LABEL_MAPPING, TREATMENT_MAPPING


def perform_plots(df, group_orders):
    treatment_labels = []
    variable_labels = []
    energy_components = {
        'backend': [],
        'embedding': [],
        'generation': [],
        'db': [],
        'reranking': [],
        'system': [],
        'other': []
    }
    energy_total_means = []

    # Create groupby objects for each component
    grouped_data = {
        'total': df.groupby(["treatment", "variable"])["energy_total"],
        'backend': df.groupby(["treatment", "variable"])["backend_energy"],
        'embedding': df.groupby(["treatment", "variable"])["embedding_energy"],
        'generation': df.groupby(["treatment", "variable"])["generation_energy"],
        'db': df.groupby(["treatment", "variable"])["db_energy"],
        'reranking': df.groupby(["treatment", "variable"])["reranking_energy"],
        'system': df.groupby(["treatment", "variable"])["system_processes_energy"]
    }

    for group in group_orders:
        for group_t, group_vs in group.items():
            for group_v in group_vs:
                # Get values for each component
                component_values = {}

                value_other = 0.0
                for component, grouped in grouped_data.items():
                    if component == 'total':
                        energy_total_mean_value = np.mean(grouped.get_group((group_t, group_v))) / 1000
                        energy_total_means.append(energy_total_mean_value)
                        value_other += energy_total_mean_value
                    else:
                        energy_component_mean_value = np.mean(grouped.get_group((group_t, group_v))) / 1000
                        component_values[component] = energy_component_mean_value
                        value_other -= energy_component_mean_value

                # Append to lists
                treatment_labels.append(TREATMENT_MAPPING.get(group_t, group_t))
                variable_labels.append(LABEL_MAPPING.get(group_v, group_v))

                component_values['other'] = value_other

                for component, values in energy_components.items():
                    values.append(component_values[component])

    # Create component labels mapping
    component_labels = {
        'backend': 'Backend',
        'embedding': 'Embedding',
        'generation': 'Generation',
        'db': 'Database',
        'reranking': 'Reranking',
        'system': 'System',
        'other': 'Other'
    }

    # Prepare the energy components dictionary in the required format
    plot_components = {
        k: v for k, v in energy_components.items() if any(v)  # Only include components with data
    }

    # Call the plotting function
    plot_energy_breakdown(
        energy_components=plot_components,
        energy_total_means=energy_total_means,
        treatment_labels=treatment_labels,
        variable_labels=variable_labels,
        component_labels=component_labels,
        figsize=(12, 6)
    )


group_orders = [
    {"t1": ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"]},
    {"t2": ["reranking_bm25s"]},
    {"t3": ["embedding_768", "embedding_384"]},
    {"t4": ["indexing_ivfflat", "indexing_hnsw"]},
    {"t6": ["caching_prefix"]},
]

base_dir = "../results/output_with_ram"
df = load_to_df(base_dir)
perform_plots(df, group_orders)