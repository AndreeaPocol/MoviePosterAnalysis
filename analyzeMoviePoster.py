from deepface import DeepFace
import cv2
import sys
from deepface.detectors import FaceDetector
from mtcnn import MTCNN
from collections import defaultdict
import requests
from PIL import Image
from io import BytesIO
import json
import os
from multiprocessing import Pool


AVAILABLE_CPUS = os.cpu_count() - 1
if AVAILABLE_CPUS == 0:
    AVAILABLE_CPUS = 1

AGES = {}
RACES = {}
GENDERS = {}
NOFACES = []

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

def writeDictToCsv(my_dict, filename):
    with open(filename, 'w') as f:
        for key in my_dict.keys():
            f.write("%s,%s\n"%(key,my_dict[key]))


def detectFaces(img):
    detector = MTCNN()
    faces = detector.detect_faces(img)
    count = 0
    for face in faces:
        x, y, w, h = face["box"]
        theface = img[int(y):int(y+h), int(x):int(x+w)]
        path = "face" + str(count) + ".png"
        cv2.imwrite( path, theface )
        count = count + 1
        # do something


def analyzePoster(movies):
    ages = defaultdict(int)
    races = defaultdict(int)
    genders = defaultdict(int)
    posters_without_faces = []

    for movie in movies:
        try:
            url = movie[1]['Poster']
            tconst = movie[0]
            poster = requests.get(url)
            filePath = f"{tconst}.png"
            img = Image.open(BytesIO(poster.content))
            # img.show()
            img.save(filePath)
            analysis = DeepFace.analyze(
                img_path = filePath, 
                enforce_detection = True,
                actions = ["age", "gender", "race"],
                detector_backend = backends[3]
            )
            for face_analysis in analysis:
                age = face_analysis['age']
                gender = face_analysis['dominant_gender']
                race = face_analysis['dominant_race']
                print(f"Detected a {age}-year-old {race.lower()} {gender.lower()}...")
                ages[age] += 1
                genders[gender] += 1
                races[race] += 1
        except Exception:
            print(f"Unable to detect face for {tconst}...")
            posters_without_faces.append(tconst)
    return ages, races, genders, posters_without_faces


def main():
    global AGES
    global RACES
    global GENDERS
    global NOFACES
    movieFile = ""

    if len(sys.argv) == 2:
        movieFile = sys.argv[1]
    else:
        print(
            "Usage: {name} [ movieFile ]".format(
                name=sys.argv[0]
            )
        )
        exit()
    
    with open(movieFile) as f:
        movies = json.load(f)

    # chunk movies into AVAILABLE_CPUS of work
    startAt = 0
    endAt = 3 #232430
    numToProcess = endAt - startAt
    numMoviesPerChunk = (int)(numToProcess / AVAILABLE_CPUS) + 1
    print(f"Number of movies per chunk: {numMoviesPerChunk}")
    moviesChunked = [list(movies.items())[i:i + numMoviesPerChunk] for i in range(startAt, endAt, numMoviesPerChunk)]
    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(analyzePoster, moviesChunked)
    pool.close()
    pool.join()

    # JOIN all dictionaries into ONE
    for result in results:
        AGES |= result[0]
        RACES |= result[1]
        GENDERS |= result[2]
        NOFACES += result[3]

    writeDictToCsv(AGES, f"ages{endAt}.csv")
    writeDictToCsv(RACES, f"races{endAt}.csv")
    writeDictToCsv(GENDERS, f"genders{endAt}.csv")
    with open(f"noFaces{endAt}.txt",'w') as tfile:
        tfile.write('\n'.join(NOFACES))

if __name__ == "__main__":
    main()