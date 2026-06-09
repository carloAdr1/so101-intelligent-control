import cv2

cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, frame = cap.read()

if ret:
    # prueba 1: voltear vertical
    fixed = cv2.flip(frame, 1)

    cv2.imwrite("fixed_cam.jpg", fixed)
    print("saved fixed_cam.jpg")
else:
    print("failed")

cap.release()
