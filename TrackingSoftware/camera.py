import cv2

ds_factor=1 #change this value if you want to scale the video stream
baseLineHeight = 215
headLineHeight = 181
width = 600 # *3
height = 360 # *3
fgbg = cv2.createBackgroundSubtractorMOG2()


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        image = cv2.resize(image, (width, height))
        image=cv2.rotate(image, cv2.ROTATE_180) #if the video feed is upside down, remove this line
        cv2.line(image, (0,baseLineHeight), (width,baseLineHeight), (255,255,255),thickness=1)
        cv2.line(image, (0,headLineHeight), (width,headLineHeight), (255,255,255),thickness=1)
        cv2.line(image, ((width/2),0), ((width/2),height), (255,255,255),thickness=1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()