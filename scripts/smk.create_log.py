import numpy as np
import pandas as pd

pre_df = pd.read_csv(snakemake.input.pre, sep = "\t")
map_df = pd.read_csv(snakemake.input.mapping, sep = "\t")
df = pd.merge(pre_df, map_df, on = "Sample", how = "inner")
df = df[["Sample", "Mean length of reads", "Number of raw reads", "Number of filtered reads", \
         "Number of mapped read", "Alignment rate"]]

df.to_csv(snakemake.output[0], sep = "\t", index = None)
