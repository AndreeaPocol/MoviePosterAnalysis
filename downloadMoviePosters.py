import sys
import requests
from PIL import Image
from io import BytesIO
import json
import os
from multiprocessing import Pool

AVAILABLE_CPUS = os.cpu_count() - 1
if AVAILABLE_CPUS == 0:
    AVAILABLE_CPUS = 1

movieFile = ""
postersFolder = ""

if len(sys.argv) == 3:
    movieFile = sys.argv[1]
    postersFolder = sys.argv[2]
else:
    print(
        "Usage: {name} [ movieFile downloadFolder]".format(
            name=sys.argv[0]
        )
    )
    exit()


def downloadPosters(movies):
    problematicPosters = []
    for movie in movies:
        try:
            url = movie[1]['Poster']
            if url == "N/A":
                continue
            tconst = movie[0]
            poster = requests.get(url, timeout=100)
            filePath = f"{postersFolder}/{tconst}.png"
            img = Image.open(BytesIO(poster.content))
            # img.show()
            img.save(filePath)
        except requests.Timeout:
            print(f'Connection dropped while processing {tconst}')
            problematicPosters.append(tconst)
        except Exception:
            print(f"Unable to download poster for {tconst} to {filePath}...")
            problematicPosters.append(tconst)
    return problematicPosters


def main():
    PROBLEMPOSTERS = []

    with open(movieFile) as f:
        movies = json.load(f)

    # chunk movies into AVAILABLE_CPUS of work
    startAt = 0
    endAt = 464861
    numToProcess = endAt - startAt
    numMoviesPerChunk = (int)(numToProcess / AVAILABLE_CPUS) + 1
    print(f"Number of movies per chunk: {numMoviesPerChunk}")
    moviesChunked = [list(movies.items())[i:i + numMoviesPerChunk] for i in range(startAt, endAt, numMoviesPerChunk)]
    
    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(downloadPosters, moviesChunked)
    pool.close()
    pool.join()

    for result in results:
        PROBLEMPOSTERS += result

    with open(f"problematic-posters.txt",'w') as tfile:
        tfile.write('\n'.join(PROBLEMPOSTERS))
    

if __name__ == "__main__":
    main()