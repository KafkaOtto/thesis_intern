from read_to_df import load_to_df
from load_plots import load_box_plot

base_dir = "../results/output_with_ram"

df = load_to_df(base_dir)
load_box_plot(df)
# print(df.to_markdown())


{
    "t1": ["control", "thresholds_0.68", "thresholds_0.78", "thresholds_0.88"],
"t2": ["control", "reranking_bm25s"],
"t3": ["control", "embedding_768", "embedding_384"],
"t4": ["control", "indexing_hnsw", "indexing_ixfflat"],
"t6": ["control", "caching_prefix"],
}