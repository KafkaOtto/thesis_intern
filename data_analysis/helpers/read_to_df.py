from .utils import load_processes_energy_count, load_answer_scores_count, load_energy_count, load_latency_count, load_accuracy_count, load_json_file
import os
import pandas as pd
from .utils import RED, RESET

exclude_runs = {
}

def check_llm_fail(base_dir):
    file_pattern = f"RAG_batch_%s_prod_%s.json"

    columns = ['treatment', 'variable', 'run', 'energy consumption', 'accuracy', 'latency']
    df = pd.DataFrame(columns=columns)

    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)

        all_runs = os.listdir(subfolder_path)

        for run in all_runs:

            folder_treatment, folder_variable = subfolder.split("_", 1)

            if (folder_variable in exclude_runs.keys()) and (run in exclude_runs[folder_variable]):
                continue

            accuracy_file = os.path.join(subfolder_path, run, file_pattern % (subfolder, "accuracies"))

            accuracy_data = load_json_file(accuracy_file)
            if accuracy_data is not None:
                for result in accuracy_data:
                    explanation = result["explanation"]
                    if "LLM request failed" in explanation:
                        print(f"{RED}current treatment: {folder_treatment}, {folder_variable}, {run} has fail accuracy request {RESET}")
                        break
    return df



def load_to_df(base_dir):
    file_pattern = "RAG_batch_%s_prod_%s.json"
    columns = [
        'treatment', 'variable', 'run',
        'energy_total', 'energy_gpu', 'energy_dram', 'energy_other', 'energy_package',
        'generation_energy', 'db_energy', 'reranking_energy', 'embedding_energy',
        'backend_energy', 'system_processes_energy',
        'accuracy', 'latency'
    ]
    df = pd.DataFrame(columns=columns)

    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        try:
            folder_treatment, folder_variable = subfolder.split("_", 1)
        except ValueError:
            print(f"Skipping folder {subfolder}, invalid format")
            continue

        all_runs = os.listdir(subfolder_path)
        for run in all_runs:
            if (folder_variable in exclude_runs) and (run in exclude_runs[folder_variable]):
                continue

            def build_path(metric):
                return os.path.join(subfolder_path, run, file_pattern % (subfolder, metric))

            file_paths = {
                "total_energy": build_path("energy_total"),
                "gpu_energy": build_path("energy_gpu"),
                "dram_energy": build_path("energy_dram"),
                "other_energy": build_path("energy_other"),
                "package_energy": build_path("energy_package"),
                "summary": build_path("summary"),
                "accuracy": build_path("accuracies"),
            }

            # Initialize all values
            item_total_energy = item_gpu_energy = item_dram_energy = item_other_energy = item_package_energy = None
            item_generation_energy = item_db_energy = item_reranking_energy = item_embedding_energy = item_backend_energy = item_system_processes_energy= None
            item_latency = item_accuracy = None

            # Load energy files
            energy_data = {
                "total_energy": load_json_file(file_paths["total_energy"]),
                "gpu_energy": load_json_file(file_paths["gpu_energy"]),
                "dram_energy": load_json_file(file_paths["dram_energy"]),
                "other_energy": load_json_file(file_paths["other_energy"]),
                "package_energy": load_json_file(file_paths["package_energy"]),
            }

            if energy_data["total_energy"] is not None:
                item_total_energy, item_generation_energy, item_db_energy, item_reranking_energy, item_embedding_energy, item_backend_energy, item_system_processes_energy = load_processes_energy_count(energy_data["total_energy"])
            if energy_data["gpu_energy"] is not None:
                item_gpu_energy = load_energy_count(energy_data["gpu_energy"])
            if energy_data["dram_energy"] is not None:
                item_dram_energy = load_energy_count(energy_data["dram_energy"])
            if energy_data["other_energy"] is not None:
                item_other_energy = load_energy_count(energy_data["other_energy"])
            if energy_data["package_energy"] is not None:
                item_package_energy = load_energy_count(energy_data["package_energy"])

            # Load latency
            summary_data = load_json_file(file_paths["summary"])
            if summary_data is not None:
                item_latency = load_latency_count(summary_data)

            # Load accuracy
            accuracy_data = load_json_file(file_paths["accuracy"])
            if accuracy_data is not None:
                item_accuracy = load_accuracy_count(accuracy_data)

            # Only include rows with some meaningful data
            if any(val is not None for val in [
                item_total_energy, item_gpu_energy, item_dram_energy,
                item_other_energy, item_package_energy,
                item_generation_energy, item_db_energy, item_reranking_energy, item_embedding_energy, item_backend_energy, item_system_processes_energy,
                item_latency, item_accuracy
            ]):
                df.loc[len(df)] = [
                    folder_treatment, folder_variable, run,
                    item_total_energy, item_gpu_energy, item_dram_energy,
                    item_other_energy, item_package_energy,
                    item_generation_energy, item_db_energy, item_reranking_energy, item_embedding_energy,
                    item_backend_energy, item_system_processes_energy,
                    item_accuracy, item_latency
                ]
    return df

def load_accuracy_df(base_dir):
    file_pattern = "RAG_batch_%s_prod_%s.json"
    columns = [
        'treatment', 'variable', 'run',
        'perfect', 'missing', 'incorrect', 'acceptable'
    ]
    df = pd.DataFrame(columns=columns)

    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        try:
            folder_treatment, folder_variable = subfolder.split("_", 1)
        except ValueError:
            print(f"Skipping folder {subfolder}, invalid format")
            continue

        all_runs = os.listdir(subfolder_path)
        for run in all_runs:
            if (folder_variable in exclude_runs) and (run in exclude_runs[folder_variable]):
                continue

            def build_path(metric):
                return os.path.join(subfolder_path, run, file_pattern % (subfolder, metric))

            answer_file_path = build_path("accuracies")

            # Initialize all values
            item_perfect = item_missing = item_incorrect = item_acceptable = None


            # Load accuracy
            accuracy_data = load_json_file(answer_file_path)
            if accuracy_data is not None:
                item_perfect, item_missing, item_incorrect, item_acceptable = load_answer_scores_count(accuracy_data)

            # Only include rows with some meaningful data
            if any(val is not None for val in [
                item_perfect, item_missing, item_incorrect, item_acceptable
            ]):
                df.loc[len(df)] = [
                    folder_treatment, folder_variable, run,
                    item_perfect, item_missing, item_incorrect, item_acceptable
                ]
    return df

if __name__ == '__main__':
    base_dir = "../results/output_with_ram"

    df = load_to_df(base_dir)
    print(df.to_markdown())

    # check_llm_fail(base_dir)
