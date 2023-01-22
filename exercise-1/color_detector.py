#!/usr/bin/env python3

"""
This is a simple multiple color detection algorithm that I got from Geeks for Geeks here: https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/ 
"""

import cv2
import numpy as np
from time import sleep

USE_HW_ACCELERATION = True

def gst_pipeline_string():
    """
    The actual gstream pipeline string is based from duckietown's dt-duckiebot-interface here: https://github.com/duckietown/dt-duckiebot-interface/blob/3d11f3d77e2754f2a3be73e93f27c43a90eb21ec/packages/camera_driver/src/jetson_nano_camera_node.py#L178
    """

    # These values were found from the dt-duckiebot-interface repo for the camera
    # This is sport mode
    exposure_time = [100000, 80000000]
    # Camera Mode 3
    camera_mode_id = 0
    res_w = 1640
    res_h = 1232
    fps = 30


    if USE_HW_ACCELERATION:
        gst_pipeline = """nvarguscamerasrc sensor-mode={} exposuretimerange="{} {}" ! video/x-raw(memory:NVMM),width={},height={},format=NV12,framerate={}/1 ! nvjpegenc ! appsink""".format(
            camera_mode_id, *exposure_time, res_w, res_h, fps
        )
    else:
        gst_pipeline = """nvarguscamerasrc sensor-mode={} exposuretimerange='{} {}' ! 'video/x-raw(memory:NVMM),width={},height={},format=NV12,framerate={}/1' ! nvvidconv ! 'video/x-raw,format=BGRx' ! videoconvert ! appsink""".format(
            camera_mode_id, *exposure_time, res_w, res_h, fps
        )
    print(f"Using GST pipeline: {gst_pipeline}")
    return gst_pipeline


camera = cv2.VideoCapture()
camera.open(gst_pipeline_string(), cv2.CAP_GSTREAMER)

if not camera.isOpened():
    print("Camera cannot be opened")

while(True):
    ret, image_frame = camera.read()
    
    hsvFrame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # These values are from here: https://stackoverflow.com/questions/57262974/tracking-yellow-color-object-with-opencv-python
    yellow_lower = np.array([22, 93, 0], np.uint8)
    yellow_upper = np.array([45, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    kernal = np.ones((5, 5), "uint8")


    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(image_frame, image_frame, mask = red_mask)

    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(image_frame, image_frame, mask = green_mask)

    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(image_frame, image_frame, mask = blue_mask)

    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(image_frame, image_frame, mask = yellow_mask)

    # # Colour tracking stuff
    # contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300.0):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         image_frame = cv2.rectangle(image_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #         cv2.putText(image_frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    # contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300.0):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         image_frame = cv2.rectangle(image_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #         cv2.putText(image_frame, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))   

    # contour, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300.0):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         image_frame = cv2.rectangle(image_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #         cv2.putText(image_frame, "Blue", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300.0):
            x, y, w, h = cv2.boundingRect(contour)
            image_frame = cv2.rectangle(image_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(image_frame, "Yellow", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))    
            print("Yellow: ", x,y,w,h)
    
    # sleep(1)
    
    # cv2.imshow("Red Colour", red_mask)
#    cv2.imshow("Multiple Color Detection in Real-Time", image_frame)
#    if cv2.waitKey(10) & 0xFF == ord('q'):
#        camera.release()
#        cv2.destroyAllWindows()
#        break
