import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########################
wCam, hCam = 640, 480
########################
volBar=400
volPrecentage = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVolume = volRange[0]
maxVolume = volRange[1]

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handDetector()

while True:
    success, img= cap.read()
    img=detector.findHands(img)

    lmlist=detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4], lmlist[5])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)

        cv2.circle(img, (cx, cy), 15, (255, 179, 0), cv2.FILLED)

        length=math.hypot(x2-x1, y2-y1)
        #print(length)

        vol = np.interp(length, [75, 280], [minVolume, maxVolume])
        volBar = np.interp(length, [75, 280], [400, 150])
        volPrecentage = np.interp(length, [75, 280], [0, 100])

        #print(vol)
        if length<=75:
            cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED)
        if length>=280:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPrecentage)} %', (40,450,), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Web Cam Feed", img)
    cv2.waitKey(1)