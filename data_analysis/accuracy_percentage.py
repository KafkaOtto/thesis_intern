from helpers.read_to_df import load_accuracy_df

base_dir = "../results/output_with_ram"

df = load_accuracy_df(base_dir)

print(df.to_markdown())