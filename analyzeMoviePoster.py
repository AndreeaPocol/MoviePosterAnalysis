from deepface import DeepFace
import cv2
import sys
from deepface.detectors import FaceDetector
from mtcnn import MTCNN
from collections import defaultdict
import glob

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
        actions = ["age", "gender", "race"],
        detector_backend = backends[3]
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
    
    paths = glob.glob(dir_path)

    for img_path in paths:
        img = cv2.imread(img_path)
        try:
            analyzePoster(img)
        except Exception:
            print(f"Unable to detect face for {img_path}")
            posters_without_faces.append(img_path)

    writeOutput(ages, "ages.csv")
    writeOutput(races, "races.csv")
    writeOutput(genders, "genders.csv")
    print(posters_without_faces)


if __name__ == "__main__":
    main()