import json
import numpy as np
import matplotlib.pyplot as plt

def run_analysis(file_path):
    print(f"opening file: {file_path} ...")
    with open(file_path, "r") as f:
        data = json.load(f)
        results = data["data"]["result"]
        total_energy = 0
        backend_energy = 0
        embedding_energy = 0
        generation_energy = 0
        db_energy = 0
        for result in results:
            item_total_energy = float(result["values"][-1][1]) - float(result["values"][0][1])
            # print("metrics:", result["metric"])
            if result["metric"]["pod_name"].startswith("llama3-1-8b"):
                generation_energy += item_total_energy
            if result["metric"]["pod_name"].startswith("pgvector"):
                db_energy += item_total_energy
            if result["metric"]["pod_name"].startswith("chat-backend"):
                backend_energy += item_total_energy
            if result["metric"]["pod_name"].startswith("e5-large-v2"):
                embedding_energy += item_total_energy
            # print("item_total_energy: ", item_total_energy)
            # if item_total_energy == 0:
            #     print("item total energy is zero", result["metric"])
            total_energy += item_total_energy
        result_arrays = [np.array(result["values"], dtype=float) for result in results]
        result_stacked = np.stack(result_arrays)
        timestamps = result_stacked[0, :, 0]
        summed_values = np.sum(result_stacked[:, :, 1], axis=0)
        print("start time: ", timestamps[0])
        print("end time: ", timestamps[-1])
        print("elapsed time: ", timestamps[-1] - timestamps[0])
        print("concerned energy: ", generation_energy + db_energy + backend_energy + embedding_energy)
        # plt.figure(figsize=(10, 5))
        # plt.plot(timestamps, summed_values, marker='o')
        # plt.xlabel('Timestamp')
        # plt.ylabel('Summed Value')
        # plt.title('Summed Values Over Time')
        # plt.grid(True)
        # plt.tight_layout()
        # plt.show()

run_analysis("input/t1_threshold/t1_threshold0.58/RAG_batch_t1_threshold0.58_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run2/RAG_batch_t1_threshold0.58_run2_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run3/RAG_batch_t1_threshold0.58_run3_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run4/RAG_batch_t1_threshold0.58_run4_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run5/RAG_batch_t1_threshold0.58_run5_prod_energy.json")
run_analysis("input/base/base_run2/RAG_batch_base_model_2_prod_energy.json")
run_analysis("input/base/base_run1/RAG_batch_base_model_1_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_1/RAG_batch_t1_threshold0.80_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_2/RAG_batch_t1_threshold0.80_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_3/RAG_batch_t1_threshold0.80_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_4/RAG_batch_t1_threshold0.80_prod_energy.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_5/RAG_batch_t1_threshold0.80_prod_energy.json")

run_analysis("input/t1_threshold/t1_threshold0.88/run_1/RAG_batch_t1_threshold0.88_prod_energy.json")