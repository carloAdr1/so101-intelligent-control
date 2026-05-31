#!/bin/bash
# Run in WSL after attaching cameras from Windows PowerShell:
#   usbipd attach --wsl --busid 1-1
#   usbipd attach --wsl --busid 2-2
sudo chmod 666 /dev/video0 /dev/video1 /dev/video2 /dev/video3
python -c "
import cv2
cap0 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)
ret0, _ = cap0.read()
ret2, _ = cap2.read()
print('cam0 (front):', ret0)
print('cam2 (side): ', ret2)
cap0.release()
cap2.release()
print('OK - ready to record' if ret0 and ret2 else 'ERROR - check USB attach')
"
