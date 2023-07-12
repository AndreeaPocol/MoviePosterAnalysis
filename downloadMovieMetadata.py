from tqdm import tqdm
import requests
import json
import requests
import threading

maxthreads = 1000
sema = threading.Semaphore(value=maxthreads)
data = dict()
problematic = []
connectionDropped = []
key = "1844b7ba"


def make_request(tid):
    sema.acquire()
    try:
        print(f"Processing {tid}...")
        data[tid] = requests.get(
            "http://www.omdbapi.com/", 
            params={"apikey": key, "i": tid}, 
            timeout=200
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
    sema.release()


def main():
    with open("tconsts.txt") as f:
        tconsts = f.read().splitlines()

    # Create and start threads for each URL
    threads = []
    for tid in tconsts:
        thread = threading.Thread(target=make_request, args=(tid,))
        thread.start()
        threads.append(thread)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Ready to write files...")
    with open("omdb_movies.json", "w") as f:
        json.dump(data, f)

    with open("problematic_tconsts.txt", "w") as f:
        f.write("\n".join(problematic))
        
    with open("connection_dropped_tconsts.txt", "w") as f:
        f.write("\n".join(connectionDropped))

if __name__ == "__main__":
    main()