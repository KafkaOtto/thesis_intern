import numpy as np

import pandas as pd
from read_to_df import load_to_df


metrics = ["energy", "responses", "accuracies"]

treatments = {
    "t1": ["thresholds_base0.58", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"],
    "t2": ["emb_768", "emb_384"],
    # "t3": ["deepseek_llama"],
    "t4": ["hnsw", "ivfflat"],
    "t5": ["caching_prefix"]
}

base_dir = "../results/output_with_ram"

df = load_to_df(base_dir)
print(df.to_markdown())
