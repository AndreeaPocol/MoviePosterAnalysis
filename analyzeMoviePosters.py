from deepface import DeepFace
import cv2
import sys
from deepface.detectors import FaceDetector
from mtcnn import MTCNN
import glob
import os
from multiprocessing import Pool
from collections import Counter

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
    ages = Counter({})
    races = Counter({})
    genders = Counter({})
    posters_without_faces = []

    for movie in movies:
        try:
            analysis = DeepFace.analyze(
                img_path = movie, 
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
            print(f"Unable to detect face for {movie}...")
            posters_without_faces.append(movie)
    return ages, races, genders, posters_without_faces


def main():
    AGES = Counter({})
    RACES = Counter({})
    GENDERS = Counter({})
    NOFACES = []

    dir_path = ""
    if len(sys.argv) == 2:
        dir_path = sys.argv[1]
    else:
        print(
            "Usage: {name} [ analyzeMoviePoster ]".format(
                name=sys.argv[0]
            )
        )
        exit()
    
    paths = glob.glob(f"{dir_path}/*")

    # chunk movies into AVAILABLE_CPUS of work
    startAt = 0
    endAt = 10 #232430
    numToProcess = endAt - startAt
    numMoviesPerChunk = (int)(numToProcess / AVAILABLE_CPUS) + 1
    print(f"Number of movies per chunk: {numMoviesPerChunk}")
    moviesChunked = [paths[i:i + numMoviesPerChunk] for i in range(startAt, endAt, numMoviesPerChunk)]
    pool = Pool(processes=AVAILABLE_CPUS)
    results = pool.map(analyzePoster, moviesChunked)
    pool.close()
    pool.join()

    # JOIN all dictionaries into ONE
    for result in results:
        AGES += result[0]
        RACES += result[1]
        GENDERS += result[2]
        NOFACES += result[3]

    writeDictToCsv(AGES, f"ages{endAt}.csv")
    writeDictToCsv(RACES, f"races{endAt}.csv")
    writeDictToCsv(GENDERS, f"genders{endAt}.csv")
    with open(f"noFaces{endAt}.txt",'w') as tfile:
        tfile.write('\n'.join(NOFACES))

if __name__ == "__main__":
    main()