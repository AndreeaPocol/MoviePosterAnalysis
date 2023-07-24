from deepface import DeepFace
import cv2
import sys
from deepface.detectors import FaceDetector
from mtcnn import MTCNN
import glob
import os
from multiprocessing import Pool
import json
import csv

AVAILABLE_CPUS = os.cpu_count() - 1
if AVAILABLE_CPUS == 0:
    AVAILABLE_CPUS = 1

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

header = [
    'id',
    'title',
    'year',
    'genre',
    'country',
    'children',
    'adolescents',
    'adults',
    'older-adults',
    'asians',
    'indians',
    'blacks',
    'whites',
    'middle-easterns',
    'latino-hispanics',
    'men',
    'women'
]

headerDetailed = [
    'id',
    'title',
    'year',
    'genre',
    'country',
    'age',
    'race',
    'gender'
]

posterDir = ""
movieDataFile = ""
if len(sys.argv) == 3:
    posterDir = sys.argv[1]
    movieDataFile = sys.argv[2]
else:
    print(
        "Usage: {name} [ analyzeMoviePoster posterDir metadataFile]".format(
            name=sys.argv[0]
        )
    )
    exit()
paths = glob.glob(f"{posterDir}/*")
with open(movieDataFile) as json_file:
    movieData = json.load(json_file)


def ageBracket(age):
    if age <= 12:
        return "children"
    elif age <= 17:
        return "adolescents"
    elif age <= 65:
        return "adults"
    else:
        return "older-adults"


def analyzePoster(movies):
    posters_without_faces = []

    file = open(f"{str(os.getpid())}-diversity-dataset.csv", 'a')
    writer = csv.writer(file)
    writer.writerow(header)
    
    fileDetailed = open(f"{str(os.getpid())}-diversity-dataset-detailed.csv", 'a')
    writerDetailed = csv.writer(fileDetailed)
    writerDetailed.writerow(headerDetailed)

    for movie in movies:
        # deepface classifications
        # https://github.com/serengil/deepface/tree/1321435a303f21e39cb7f0fff67582449768846f/deepface/extendedmodels
        agesInThisPoster = {"children": 0, "adolescents": 0, "adults": 0, "older-adults": 0}
        racesInThisPoster = {"asian": 0, "indian": 0, "black": 0, "white": 0, "middle eastern": 0, "latino hispanic": 0}
        gendersInThisPoster = {"Woman": 0, "Man": 0}
        try:
            analysis = DeepFace.analyze(
                img_path = movie, 
                enforce_detection = True,
                actions = ["age", "gender", "race"],
                detector_backend = backends[3]
            )

            tconst = os.path.splitext(os.path.basename(movie))[0]
            metadata = movieData[tconst]

            for face_analysis in analysis:
                age = face_analysis['age']
                gender = face_analysis['dominant_gender']
                race = face_analysis['dominant_race']
                print(f"Detected a {age}-year-old {race.lower()} {gender.lower()}...")
                agesInThisPoster[ageBracket(age)] += 1
                gendersInThisPoster[gender] += 1
                racesInThisPoster[race] += 1
                csvRowDetailed = [
                    tconst,
                    metadata['Title'],
                    metadata['Year'],
                    metadata['Genre'],
                    metadata['Country'],
                    age,
                    gender,
                    race
                ]
                writerDetailed.writerows(csvRowDetailed)  

            csvRow = [
                tconst,
                metadata['Title'],
                metadata['Year'],
                metadata['Genre'],
                metadata['Country'],
                agesInThisPoster["children"],
                agesInThisPoster["adolescents"],
                agesInThisPoster["adults"],
                agesInThisPoster["older-adults"],
                racesInThisPoster["asian"],
                racesInThisPoster["indian"],
                racesInThisPoster["black"],
                racesInThisPoster["white"],
                racesInThisPoster["middle eastern"],
                racesInThisPoster["latino hispanic"],
                gendersInThisPoster["Man"],
                gendersInThisPoster["Woman"]
            ]
            writer.writerows(csvRow)

        except Exception:
            print(f"Unable to process {movie}...")
            posters_without_faces.append(movie)
    return posters_without_faces


def main():
    NOFACES = []

    # chunk the first half of the movies into AVAILABLE_CPUS of work
    startAt = 0 #232430
    endAt = 232430 #464861
    numToProcess = endAt - startAt
    numMoviesPerChunk = (int)(numToProcess / AVAILABLE_CPUS) + 1
    print(f"Number of movies per chunk: {numMoviesPerChunk}")
    moviesChunked = [paths[i:i + numMoviesPerChunk] for i in range(startAt, endAt, numMoviesPerChunk)]
    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(analyzePoster, moviesChunked)
    pool.close()
    pool.join()

    for result in results:
        NOFACES += result[0]
    
    # TODO: garbage collect (here?)

    # chunk the second half of the movies into AVAILABLE_CPUS of work
    startAt = 232430
    endAt = 464862
    numToProcess = endAt - startAt
    numMoviesPerChunk = (int)(numToProcess / AVAILABLE_CPUS) + 1
    print(f"Number of movies per chunk: {numMoviesPerChunk}")
    moviesChunked = [paths[i:i + numMoviesPerChunk] for i in range(startAt, endAt, numMoviesPerChunk)]
    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(analyzePoster, moviesChunked)
    pool.close()
    pool.join()

    for result in results:
        NOFACES += result[0]

    with open("no_faces.txt",'w') as tfile:
        tfile.write('\n'.join(NOFACES))


if __name__ == "__main__":
    main()