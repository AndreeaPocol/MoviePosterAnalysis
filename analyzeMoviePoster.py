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


ages = defaultdict(int)
races = defaultdict(int)
genders = defaultdict(int)

posters_without_faces = []
backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

def writeOutput(my_dict, filename):
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


def analyzePoster(img):
    analysis = DeepFace.analyze(
        img_path = img, 
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


def main():
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

    for movie in movies:
        url = movie['Poster']
        name = movie['Title']
        poster = requests.get(url)
        img = Image.open(BytesIO(poster.content))
        try:
            analyzePoster(img)
        except Exception:
            print(f"Unable to detect face for {name}")
            posters_without_faces.append(name)

    writeOutput(ages, "ages.csv")
    writeOutput(races, "races.csv")
    writeOutput(genders, "genders.csv")
    print("Could not detect faces for: ", posters_without_faces)


if __name__ == "__main__":
    main()