from deepface import DeepFace
import cv2
import sys
from deepface.detectors import FaceDetector
from mtcnn import MTCNN
from collections import defaultdict
import pandas as pd

ages = defaultdict(int)
races = defaultdict(int)
genders = defaultdict(int)

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


def detectFaces():
    detector = MTCNN()
    faces = detector.detect_faces( img )
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
        actions = ["age", "gender", "race"]
    )
    for face_analysis in analysis:
        age = face_analysis['age']
        gender = face_analysis['dominant_gender']
        race = face_analysis['dominant_race']
        print(age, gender, race)
        ages[age] += 1
        genders[gender] += 1
        races[race] += 1


def main():
    img_path = ""
    if len(sys.argv) == 2:
        img_path = sys.argv[1]
    else:
        print(
            "Usage: {name} [ analyzeMoviePoster ]".format(
                name=sys.argv[0]
            )
        )
        exit()
    
    img = cv2.imread(img_path)
    analyzePoster(img)

    writeOutput(ages, "ages.csv")
    writeOutput(races, "races.csv")
    writeOutput(genders, "genders.csv")


if __name__ == "__main__":
    main()