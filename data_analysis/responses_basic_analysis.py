import json
import matplotlib.pyplot as plt
import os
from datetime import datetime

def run_analysis(file_path):
    print(f"opening file: {file_path} ...")
    response_file = file_path.format("responses")
    summary_file = file_path.format("summary")
    with open(response_file, "r") as response_f:
        with open(summary_file, "r") as summary_f:
            responses = json.load(response_f)
            summaries = json.load(summary_f)
            print("experiment start time", datetime.fromtimestamp(summaries['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
            print("experiment end time", datetime.fromtimestamp(summaries['end_time']).strftime('%Y-%m-%d %H:%M:%S'))
            print("query size", len(responses))
            latencies = []
            for response in responses:
                latency = response["metrics"]["end_to_end_latency_s"]
                latencies.append(latency)

                # if latency > 8:
                #     query = response["request_config"]['prompt'][0]
                #     print("There is latency > 100")
                #     print("query:", query)
                #     print("answer:", response["generated_text"])

            total_latency = sum(latencies)
            print("Total latency:", total_latency)
            print("------------------------------")

            # Draw sequence diagram (simple line plot)
            plt.figure(figsize=(12, 6))
            plt.plot(latencies, marker='o', linestyle='-')
            plt.title("End-to-End Latency per Query")
            plt.xlabel("Query Index")
            plt.ylabel("Latency (s)")
            plt.grid(True)
            plt.tight_layout()
            # plt.show()
            base_name = os.path.basename(response_file)
            plt.savefig(f"figures/{base_name}.png")


run_analysis("input/t1_threshold/t1_threshold0.58/RAG_batch_t1_threshold0.58_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run2/RAG_batch_t1_threshold0.58_run2_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run3/RAG_batch_t1_threshold0.58_run3_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run4/RAG_batch_t1_threshold0.58_run4_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.58_run5/RAG_batch_t1_threshold0.58_run5_prod_{}.json")
run_analysis("input/base/base_run2/RAG_batch_base_model_2_prod_{}.json")
run_analysis("input/base/base_run1/RAG_batch_base_model_1_prod_{}.json")
run_analysis("input/base/base_run3/RAG_batch_base_run3_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_1/RAG_batch_t1_threshold0.80_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_2/RAG_batch_t1_threshold0.80_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_3/RAG_batch_t1_threshold0.80_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_4/RAG_batch_t1_threshold0.80_prod_{}.json")
run_analysis("input/t1_threshold/t1_threshold0.80/run_5/RAG_batch_t1_threshold0.80_prod_{}.json")

run_analysis("input/t1_threshold/t1_threshold0.88/run_1/RAG_batch_t1_threshold0.88_prod_{}.json")