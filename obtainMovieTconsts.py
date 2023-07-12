import pandas as pd
import numpy as np

basics = pd.read_csv("title.basics.tsv", delimiter="\t")
basics["startYear"] = basics["startYear"].astype(str).replace("\\N", np.NaN).astype(float)
filter_data = basics[(basics["titleType"] == "movie") & (basics["startYear"] >= 1960)]

print(filter_data[filter_data["tconst"] == "tt0015414"]) # example

with open("tconsts_small.txt", "w") as f: # example
    f.write("\n".join(filter_data["tconst"][1:10].tolist()))

with open("tconsts.txt", "w") as f:
    f.write("\n".join(filter_data["tconst"].tolist()))