"""
ROI calibration script for HSV-based cable color detection.

Reads pre-captured reference images from /tmp/ and computes pixel
counts for black (V<40) and white (V>200, S<25) masks within the
defined region of interest. Used to calibrate detection thresholds.

Usage:
    python scripts/calibrar_roi.py
"""
import cv2
import numpy as np

ROI = (0, 270, 220, 450)

for nombre, path in [("only_black", "/tmp/sit1_only_black.jpg"),
                     ("only_white", "/tmp/sit2_only_white.jpg"),
                     ("both_bw",    "/tmp/sit3_both_bw.jpg")]:
    img = cv2.imread(path)
    if img is None:
        print(nombre + ": no encontrada")
        continue
    x1,y1,x2,y2 = ROI
    roi = img[y1:y2, x1:x2]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask_negro  = cv2.inRange(hsv, np.array([0,0,0]),   np.array([180,255,40]))
    mask_blanco = cv2.inRange(hsv, np.array([0,0,200]), np.array([180,25,255]))
    print(nombre + ": negro=" + str(cv2.countNonZero(mask_negro)) +
          ", blanco=" + str(cv2.countNonZero(mask_blanco)))
