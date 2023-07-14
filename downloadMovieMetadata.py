import requests
import json
import requests
import os
from multiprocessing import Pool

data = dict()
problematic = []
connectionDropped = []
key = "1844b7ba"

AVAILABLE_CPUS = os.cpu_count() - 1
if AVAILABLE_CPUS == 0:
    AVAILABLE_CPUS = 1

def make_request(tid):
    try:
        data[tid] = requests.get(
            "http://www.omdbapi.com/", 
            params={"apikey": key, "i": tid}, 
            timeout=200
        ).json()
        print(f"Successfully processed {tid}...")
    except json.JSONDecodeError:
        try:
            data[tid] = json.loads(
                requests.get(
                    "http://www.omdbapi.com/",
                    params={"apikey": key, "i": tid},
                ).text.replace("\\", "\\\\")
            )
        except Exception:
            print(f'JSON decode error occured while processing {tid}')
            problematic.append(tid) 
    except requests.Timeout:
        print(f'Connection dropped while processing {tid}')
        problematic.append(tid)
    except Exception:
        print(f'Unknown error occured while processing {tid}')
        problematic.append(tid)


def main():
    with open("tconsts_small.txt") as f:
        tconsts = f.read().splitlines()

    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(make_request, tconsts[:250000])
    pool.close()
    pool.join()

    print("Ready to write files...")
    with open("omdb_movies.json", "w") as f:
        json.dump(data, f)

    with open("problematic_tconsts.txt", "w") as f:
        f.write("\n".join(problematic))
        
    with open("connection_dropped_tconsts.txt", "w") as f:
        f.write("\n".join(connectionDropped))

if __name__ == "__main__":
    main()