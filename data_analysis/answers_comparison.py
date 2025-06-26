import json
import matplotlib.pyplot as plt
import os

def run_analysis(base_file, to_file):
    with open(base_file, "r") as base_f:
        with open(to_file, "r") as to_f:
            base_responses = json.load(base_f)
            to_responses = json.load(to_f)
            print("base size", len(base_responses))
            print("to size", len(to_responses))
            i = 0
            for base_response in base_responses:
                query = base_response["request_config"]['prompt'][0]
                base_generated_text = base_response["generated_text"]
                to_generated_text = to_responses[i]["generated_text"]
                i += 1
                if base_generated_text != to_generated_text:
                    print("different answer for query: ", query)
                    print("base answer: ", base_generated_text)
                    print("to answer: ", to_generated_text)
            print("-----------", i)


run_analysis("input/t1_threshold/t1_threshold0.58/RAG_batch_t1_threshold0.58_prod_responses.json",
             "input/t1_threshold/t1_threshold0.58_run2/RAG_batch_t1_threshold0.58_run2_prod_responses.json")
run_analysis("input/t1_threshold/t1_threshold0.58/RAG_batch_t1_threshold0.58_prod_responses.json",
             "input/t1_threshold/t1_threshold0.58_run3/RAG_batch_t1_threshold0.58_run3_prod_responses.json")
run_analysis("input/t1_threshold/t1_threshold0.58/RAG_batch_t1_threshold0.58_prod_responses.json",
             "input/t1_threshold/t1_threshold0.58_run4/RAG_batch_t1_threshold0.58_run4_prod_responses.json")
run_analysis("input/t1_threshold/t1_threshold0.58/RAG_batch_t1_threshold0.58_prod_responses.json",
             "input/t1_threshold/t1_threshold0.58_run5/RAG_batch_t1_threshold0.58_run5_prod_responses.json")