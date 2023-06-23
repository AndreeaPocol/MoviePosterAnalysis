from deepface import DeepFace
import cv2
import sys
from deepface.detectors import FaceDetector
from mtcnn import MTCNN


backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

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
        actions = ["age", "gender", "emotion", "race"]
    ) 
    print(analysis)


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
    
    img = cv2.imread( img_path )
    analyzePoster(img)

if __name__ == "__main__":
    main()