from tqdm import tqdm
import requests
import json
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

with open("tconsts.txt") as f:
    tconsts = f.read().splitlines()

data = dict()
problematic = []

for tid in tqdm(tconsts):
    try:
        data[tid] = requests.get(
            "http://www.omdbapi.com/", params={"apikey": "48d60ec2", "i": tid}
        ).json()
    except json.JSONDecodeError:
        try:
            data[tid] = json.loads(
                requests.get(
                    "http://www.omdbapi.com/",
                    params={"apikey": "48d60ec2", "i": tid},
                ).text.replace("\\", "\\\\")
            )
        except Exception:
            problematic.append(tid)
    except Exception:
        problematic.append(tid)


with open("omdb_movies.json", "w") as f:
    json.dump(data, f)


with open("problematic_tconsts.txt", "w") as f:
    f.write("\n".join(problematic))