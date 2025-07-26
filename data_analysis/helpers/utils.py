import json
import os
import bz2

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
LABEL_MAPPING = {
    "thresholds_base0.58": "base 0.58",
    "thresholds_0.68": "0.68",
    "thresholds_0.78": "0.78",
    "thresholds_0.88": "0.88",
    "embedding_768": "768",
    "embedding_384": "384",
    "indexing_ivfflat": "ivfflat",
    "indexing_hnsw": "hnsw",
    "caching_prefix": "prefix",
    "reranking_bm25s": "bm25s",
    "combination_emb384with078": "384 & 0.78",
}

TREATMENT_MAPPING = {
    "t1": "T1: thresholds",
    "t2": "T2: reranking",
    "t3": "T3: embedding",
    "t4": "T4: indexing",
    "t6": "T5: caching",
    "t7": "combo",
}

group_orders = [
    {"t1" : ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"]},
    {"t2": ["reranking_bm25s"]},
    {"t3": ["embedding_768", "embedding_384"]},
    {"t4": ["indexing_ivfflat", "indexing_hnsw"]},
    {"t6": ["caching_prefix"]},
]

group_orders_combo = [
    {"t1" : ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"]},
    {"t2": ["reranking_bm25s"]},
    {"t3": ["embedding_768", "embedding_384"]},
    {"t4": ["indexing_ivfflat", "indexing_hnsw"]},
    {"t6": ["caching_prefix"]},
    {"t7": ["combination_emb384with078"]},
]

def load_energy_count(data):
    results = data["data"]["result"]
    total_energy = 0
    for result in results:
        item_total_joules = float(result["values"][-1][1]) - float(result["values"][0][1])
        total_energy += item_total_joules
    return total_energy


def load_processes_energy_count(data):
    results = data["data"]["result"]
    total_energy = 0
    backend_energy = 0
    embedding_energy = 0
    generation_energy = 0
    db_energy = 0
    pod_energy_map = {}
    reranking_energy = 0
    system_processes_energy = 0
    for result in results:
        pod_name = result["metric"]["pod_name"]
        elapsed_seconds = float(result["values"][-1][0]) - float(result["values"][0][0])
        item_total_joules = float(result["values"][-1][1]) - float(result["values"][0][1])

        if pod_name not in pod_energy_map:
            pod_energy_map[pod_name] = 0.0
        pod_energy_map[pod_name] += item_total_joules
        # item_watts = item_total_joules / elapsed_seconds
        # print("metrics:", result["metric"])
        if pod_name.startswith("llama3") or pod_name.startswith("deepseek"):
            generation_energy += item_total_joules
        if pod_name.startswith("pgvector"):
            db_energy += item_total_joules
        if pod_name.startswith("chat-backend"):
            backend_energy += item_total_joules
        if pod_name.startswith("e5"):
            embedding_energy += item_total_joules
        if pod_name.startswith("reranker"):
            reranking_energy += item_total_joules
        if pod_name.startswith("system_processes"):
            system_processes_energy += item_total_joules
        # print("item_total_energy: ", item_total_energy)
        # if item_total_energy == 0:
        #     print("item total energy is zero", result["metric"])
        total_energy += item_total_joules
    # print("Energy usage by pod (sorted by usage):")
    # for pod, energy in sorted(pod_energy_map.items(), key=lambda x: x[1], reverse=True):
    #     print(f"  {pod}: {energy:.2f} J")
    # print("-------------------------------")
    return total_energy, generation_energy, db_energy, reranking_energy, embedding_energy, backend_energy, system_processes_energy

# def load_latency_count(data):
#     latencies = []
#     for response in data:
#         latency = response["metrics"]["end_to_end_latency_s"]
#         latencies.append(latency)
#     total_latency = sum(latencies)
#     return total_latency

def load_latency_count(data):
    num_completed_requests = data["num_completed_requests"]
    num_non_errored_requests = data["num_non_errored_requests"]
    if num_non_errored_requests != 2606:
        print("contains error request")
    if num_completed_requests != 2606:
        print("contains incomplete request")
    return (data["end_time"] - data["start_time"])

def load_accuracy_count(data):
    incorrect = 0
    perfect = 0
    missing = 0
    acceptable = 0
    total_count = len(data)
    for result in data:
        score = result["score"]
        if score == 1:
            perfect += 1
        elif score == 0.5:
            acceptable += 1
        elif score == 0:
            missing += 1
        elif score == -1:
            incorrect += 1
        else:
            print("unknown score: ", score)
    return perfect / total_count

def load_json_file(json_file):
    try:
        if os.path.exists(json_file):
            with open(json_file) as energy_file:
                json_data = json.load(energy_file)
                return json_data
        else:
            print(f"{json_file} does not exist")
    except Exception as e:
        print(f"Error loading JSON file: {json_file}: {e}")
    return None

def load_answer_scores_count(data):
    incorrect = 0
    perfect = 0
    missing = 0
    acceptable = 0
    total_count = len(data)
    for result in data:
        score = result["score"]
        if score == 1:
            perfect += 1
        elif score == 0.5:
            acceptable += 1
        elif score == 0:
            missing += 1
        elif score == -1:
            incorrect += 1
        else:
            print("unknown score: ", score)
    return perfect, missing, incorrect, acceptable

def load_answer_types(dataset_path):
    try:
        answer_type_mapping = {}
        with bz2.open(dataset_path, "rt") as file:
            for line in file:
                try:
                    item = json.loads(line)
                    answer_type_mapping[item["query"]] = {
                        "question_type": item["question_type"],
                        "static_or_dynamic": item["static_or_dynamic"],
                        "domain": item["domain"],
                    }
                except json.JSONDecodeError:
                    print("Warning: Failed to decode a line.")
            return answer_type_mapping
    except FileNotFoundError as e:
        print(f"Error: The file {dataset_path} was not found.")
        raise e
    except IOError as e:
        print(f"Error: An error occurred while reading the file {dataset_path}.")
        raise e



if __name__ == '__main__':
    # file_path = "../results/output_with_ram/t1_thresholds_0.68/run_1/RAG_batch_t1_thresholds_0.68_prod_energy_gpu.json"
    full_dataset_path = "/Users/zhinuanguo/Projects/CRAG/myown/input/crag_task_1_and_2_dev_v4.jsonl.bz2"
    answer_type_mapping = load_answer_types(full_dataset_path)
    print(f"first 10 answer types: {list(answer_type_mapping.items())[:10]}")
