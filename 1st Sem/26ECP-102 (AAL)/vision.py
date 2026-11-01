import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    result = model(frame, verbose=False)[0]
    cv2.imshow("Vision AI", result.plot())

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()