from deepface import DeepFace

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

def main():
    img = ""
    if len(sys.argv) == 2:
        img = sys.argv[1]
    else:
        print(
            "Usage: {name} [ analyzeMoviePoster ]".format(
                name=sys.argv[0]
            )
        )
        exit()
    
    print(img)
    analysis = DeepFace.analyze(
        img_path = img, 
        actions = ["age", "gender", "emotion", "race"], 
        detector_backend = backends[3]) 
    print(analysis)