import json
import os

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def load_energy_count(data):
    results = data["data"]["result"]
    total_energy = 0
    backend_energy = 0
    embedding_energy = 0
    generation_energy = 0
    db_energy = 0
    for result in results:
        elapsed_seconds = float(result["values"][-1][0]) - float(result["values"][0][0])
        item_total_joules = float(result["values"][-1][1]) - float(result["values"][0][1])
        # item_watts = item_total_joules / elapsed_seconds
        # print("metrics:", result["metric"])
        if result["metric"]["pod_name"].startswith("llama3") or result["metric"]["pod_name"].startswith("deepseek"):
            generation_energy += item_total_joules
        if result["metric"]["pod_name"].startswith("pgvector"):
            db_energy += item_total_joules
        if result["metric"]["pod_name"].startswith("chat-backend"):
            backend_energy += item_total_joules
        if result["metric"]["pod_name"].startswith("e5"):
            embedding_energy += item_total_joules
        # print("item_total_energy: ", item_total_energy)
        # if item_total_energy == 0:
        #     print("item total energy is zero", result["metric"])
        total_energy += item_total_joules
    return generation_energy + db_energy + backend_energy + embedding_energy

def load_latency_count(data):
    latencies = []
    for response in data:
        latency = response["metrics"]["end_to_end_latency_s"]
        latencies.append(latency)
    total_latency = sum(latencies)
    return total_latency

# def load_latency_count(data):
#     num_completed_requests = data["num_completed_requests"]
#     num_non_errored_requests = data["num_non_errored_requests"]
#     if num_non_errored_requests != 2606:
#         print("contains error request")
#     if num_completed_requests != 2606:
#         print("contains incomplete request")
#     return (data["end_time"] - data["start_time"])

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
    return perfect

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
