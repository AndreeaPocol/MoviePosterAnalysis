import requests
import json
from multiprocessing import Pool
from constants import key
from constants import AVAILABLE_CPUS

problematic = []


def make_request(tids):
    maxTIDS = len(tids)

    data = {}
    for i in range( 0, maxTIDS ):
        tid = tids[i]
       
        try:
            data[tid] = requests.get(
                "http://www.omdbapi.com/", 
                params={"apikey": key, "i": tid}, 
                timeout=200
            ).json()
        
            if ( i > 0 and i % 1000 == 0 ):
                print(f"Successfully processed approximately: {i} of {maxTIDS} tconsts (most recent {tid})")
              
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

    print(f"Thread done.")
    return data, problematic

def main():
    DATA = {}
    PROBLEMPOSTERS = []

    with open("tconsts.txt") as f:
        tconsts = f.read().splitlines()

    # chunk tconsts into AVAILABLE_CPUS of work
    startAt = 0 #232430
    endAt = 232430 #464862
    numToProcess = endAt - startAt
    numTCONSTPerChunk = (int)(numToProcess / AVAILABLE_CPUS) + 1
    print(numTCONSTPerChunk)

    tconstsChunked = [tconsts[i:i + numTCONSTPerChunk] for i in range(startAt, endAt, numTCONSTPerChunk )]
    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(make_request, tconstsChunked)
    pool.close()
    pool.join()

    for result in results:
        DATA |= result[0]
        PROBLEMPOSTERS += result[1]

    print("Ready to write files... with ", len( DATA.keys() ), " entries.")
    with open("omdb_movies.json", "w") as f:
        json.dump(DATA, f)
    f.close()
    
    with open("problematic_tconsts.txt", "w") as f:
        f.write("\n".join(PROBLEMPOSTERS))
    f.close()

if __name__ == "__main__":
    main()