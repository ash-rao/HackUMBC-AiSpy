from flask import Flask, render_template, Response

import cv2
from google.cloud import vision
import random 

app=Flask(__name__)
video = cv2.VideoCapture(0)
# global variable
frame = bytearray(30)

@app.route('/')
def index():
    return render_template('index.html')

def localize_objects(content):
    
    
    client = vision.ImageAnnotatorClient()

    
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    choice = random.randint(0, len(objects)-1)
    return objects[choice].name

def gen(video):
    
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #localize_objects(frame)
        #break
    
@app.route('/recieve_data')
def get_id():
  success, image = video.read()
  ret, jpeg = cv2.imencode('.jpg', image)
  frame = jpeg.tobytes()
  objectpicked = localize_objects(frame)
	
  return "<p> I SPY A " + objectpicked+ "</p>"   

	

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)




