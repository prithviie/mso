import cv2
import numpy as np
from os import system
system('clear')

def get_tracks(input_image, output_image):

    img = cv2.imread(input_image)
    # print(img.shape)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 0], dtype=np.uint8)
    upper_white = np.array([0, 0, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)

    res = cv2.bitwise_and(img,img, mask=mask)
    # cv2.imshow('img',img)
    # cv2.imshow('mask',mask)
    # cv2.imshow('res',res)

    res = cv2.bitwise_not(res)
    # res = cv2.resize(res, (0, 0), fx=1.75, fy=1.75)
    cv2.imshow('neg-res', res)

    # cv2.imwrite(output_image, res)

    cv2.waitKey(15000)
    cv2.destroyAllWindows()


get_tracks('./further_improvements/map-test.png', './further_improvements/map-test-tracks.png')