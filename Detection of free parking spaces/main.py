import cv2 as cv
import os

def getParkingSlots(connectedComponents):
    (labels, label_ids, values, centroid) = connectedComponents
    slots = []
    coef = 1
    for i in range(1, labels):
        x1 = int(values[i, cv.CC_STAT_LEFT] * coef)
        y1 = int(values[i, cv.CC_STAT_TOP] * coef)
        w = int(values[i, cv.CC_STAT_WIDTH] * coef)
        h = int(values[i, cv.CC_STAT_HEIGHT] * coef)
        slots.append([x1, y1, w, h])
    return slots

# Reading the path of the video and the mask
maskPath = os.path.join(".", "resources", "mask_crop.png")
videoPath = os.path.join(".", "resources", "parking_crop.mp4")


maskCrop = cv.imread(maskPath)
maskCrop = cv.cvtColor(maskCrop, cv.COLOR_BGR2GRAY)

connectedComponents = cv.connectedComponentsWithStats(maskCrop, 4, cv.CV_32S)
slots = getParkingSlots(connectedComponents)

parkingCrop = cv.VideoCapture(videoPath)

ret = True

while ret:
    ret, frame = parkingCrop.read()
    for slot in slots:
        x, y, w, h = slot
        cv.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
    if ret:
        cv.imshow("video", frame)
        if cv.waitKey(25) & 0xFF == ord("q"):
            break

parkingCrop.release()
cv.destroyAllWindows()