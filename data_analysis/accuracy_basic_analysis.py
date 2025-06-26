import json

def run_analysis(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load file '{file_path}': {e}")
        return

    incorrect = 0
    perfect = 0
    missing = 0
    acceptable = 0

    total_count = len(data)
    for i, result in enumerate(data):
        try:
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
                print(f"unknown score in entry {i}: {score}")
        except Exception as e:
            print(f"Error processing entry {i}: {e}")
            continue  # Skip this entry and continue with the next

    print("total_count: ", total_count)
    print("perfect: ", perfect)
    print("perfect per: ", perfect/total_count)
    print("acceptable: ", acceptable)
    print("missing: ", missing)
    print("incorrect: ", incorrect)
    print("\n")


def run_all_analyses(threshold_label):
    for i in range(1, 11):
        file_path = f"/Users/zhinuanguo/Downloads/rag_llmperf-add_rag/src/outout_archieve/{threshold_label}/run_{i}/RAG_batch_{threshold_label}_prod_accuracies.json"
        run_analysis(file_path)


run_all_analyses("t3_emb_384")
