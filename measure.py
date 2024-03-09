import cv2
import numpy as np
import math
import sys
import os

src_blue = cv2.imread("C:/Users/Roy Work/Documents/NBIL/labelme/img/label.png")
src = src_blue.copy()
width = 480
height = 480
dim = (width,height)

src = cv2.resize(src,dim,interpolation = cv2.INTER_AREA)

'''cv2.imshow('Resized Image', src)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

img = src.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(gray)



# Find contours in image
edged = cv2.Canny(src, 0, 200)
cv2.waitKey(0)
contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('Canny Edges After Contouring', edged)
cv2.waitKey(0)
print("Number of Contours found = " + str(len(contours)))

cv2.drawContours(src, contours, -1, (0, 255, 0), 3)
'''cv2.imshow('Contours', src)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

# Draw skeleton of the image on the mask
img = gray.copy()
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
ret,img = cv2.threshold(img,10,100,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False
while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy() 
    zeros = size - cv2.countNonZero(img)
    if zeros==size: done = True
kernel = np.ones((2,2), np.uint8)
skel = cv2.dilate(skel, kernel, iterations=1)
skeleton_contours, _ = cv2.findContours(skel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
largest_skeleton_contour = max(skeleton_contours, key=cv2.contourArea)
src = src_blue.copy()
cv2.drawContours(src, skeleton_contours, -1, (0, 255, 0), 3)
'''cv2.imshow('Contours', src)
cv2.waitKey(0)
cv2.destroyAllWindows()'''