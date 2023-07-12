from tqdm import tqdm
import requests
import json

key = "1844b7ba"

with open("tconsts_small.txt") as f:
    tconsts = f.read().splitlines()

data = dict()
problematic = []
connectionDropped = []

for tid in tqdm(tconsts):
    try:
        print(f"Processing {tid}...")
        data[tid] = requests.get(
            "http://www.omdbapi.com/", 
            params={"apikey": key, "i": tid}, 
            timeout=20
        ).json()
    except json.JSONDecodeError:
        try:
            data[tid] = json.loads(
                requests.get(
                    "http://www.omdbapi.com/",
                    params={"apikey": key, "i": tid},
                ).text.replace("\\", "\\\\")
            )
        except Exception:
            problematic.append(tid)
    except requests.Timeout:
        print(f'Connection dropped while processing {tid}')
        problematic.append(tid)
    except Exception:
        problematic.append(tid)


with open("omdb_movies.json", "w") as f:
    json.dump(data, f)

with open("problematic_tconsts.txt", "w") as f:
    f.write("\n".join(problematic))
    
with open("connection_dropped_tconsts.txt", "w") as f:
    f.write("\n".join(connectionDropped))