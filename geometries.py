import numpy as np
import cv2

class geometries:
	def __init__(self,image):
		self.image=image
		self.image_copy=self.image.copy() 
		self.mask=np.zeros_like(self.image_copy)

	def skeleton(self):
		size = np.size(self.image)
		skel = np.zeros(self.image.shape,np.uint8)
		_,image = cv2.threshold(self.image,10,255,cv2.THRESH_TOZERO)
		element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
		done = False
		while( not done):
			eroded = cv2.erode(image,element)
			temp = cv2.dilate(eroded,element)
			temp = cv2.subtract(image,temp)
			skel = cv2.bitwise_or(skel,temp)
			image = eroded.copy() 
			zeros = size - cv2.countNonZero(image)
			if zeros==size: done = True
		kernel = np.ones((1,1), np.uint8)
		self.skel = cv2.dilate(skel, kernel, iterations=1)
		#cv2.imshow("Show Skeleton",self.skel)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		return(self.skel)

	def largest_skeleton_contour(self,skel):
		skeleton_contours, _ = cv2.findContours(skel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		largest_skeleton_contour = max(skeleton_contours, key=cv2.contourArea)
		return(largest_skeleton_contour)


