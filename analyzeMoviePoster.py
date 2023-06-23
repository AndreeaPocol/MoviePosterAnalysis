from deepface import DeepFace
import cv2
import sys

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

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