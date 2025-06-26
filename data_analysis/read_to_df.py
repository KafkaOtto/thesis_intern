from utils import load_energy_count, load_latency_count, load_accuracy_count, load_json_file
from collections import defaultdict
import os
import pandas as pd

exclude_runs = {
    # "emb_768": ["run_1"],
    # "thresholds_base0.58": ["run_6"],
    # "caching_prefix": ["run_2"],
    # "thresholds_0.68": ["run_4", "run_6"],
#     "threshold0.88": ["run_2"],
    "reranking_bm25s": ["run_1", "run_2"],
}


def load_to_df(base_dir):
    file_pattern = f"RAG_batch_%s_prod_%s.json"
    aggregated_latencies = defaultdict(list)
    aggregated_accuracies = defaultdict(list)
    aggregated_energies= defaultdict(list)

    columns = ['treatment', 'variable', 'run', 'energy consumption', 'accuracy', 'latency']
    df = pd.DataFrame(columns=columns)

    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)

        all_runs = os.listdir(subfolder_path)

        if len(all_runs) < 10:
            print(f"current treatment: {subfolder} has less than 10 runs")

        for run in all_runs:

            # check energy
            folder_treatment, folder_variable = subfolder.split("_", 1)

            if (folder_variable in exclude_runs.keys()) and (run in exclude_runs[folder_variable]):
                continue

            energy_file = os.path.join(subfolder_path, run, file_pattern % (subfolder, "energy_total"))
            response_file = os.path.join(subfolder_path, run, file_pattern % (subfolder, "responses"))
            accuracy_file = os.path.join(subfolder_path, run, file_pattern % (subfolder, "accuracies"))

            energy_data = load_json_file(energy_file)
            item_energy = None
            item_latency = None
            item_accuracy = None

            if energy_data is not None:
                item_energy = load_energy_count(energy_data)
                aggregated_energies[f"{subfolder}"].append(item_energy)

            response_data = load_json_file(response_file)
            if response_data is not None:
                item_latency = load_latency_count(response_data)
                aggregated_latencies[f"{subfolder}"].append(item_latency)

            accuracy_data = load_json_file(accuracy_file)
            if accuracy_data is not None:
                item_accuracy = load_accuracy_count(accuracy_data)
                aggregated_accuracies[f"{subfolder}"].append(item_accuracy)

            if any(val is not None for val in [item_energy, item_latency, item_accuracy]):
                df.loc[len(df)] = [folder_treatment, folder_variable, run, item_energy, item_accuracy, item_latency]

    return df


