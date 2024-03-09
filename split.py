import cv2
import numpy as np
import math
import sys
import os

class split:
	def __init__(self,img_path):
		self.src = img_path
		#self.src = cv2.imread(img_path)

	def resize(self,width = 612,height = 512):
		self.width = width
		self.height = height
		dim = (self.width,self.height)
		self.src = cv2.resize(self.src,dim,interpolation = cv2.INTER_AREA)
		#self.gray = cv2.cvtColor(self.src,cv2.COLOR_BGR2GRAY)
		self.mask = np.zeros_like(self.src)
		return(self.src)

	def split_binary(self):
		self.b,self.g,self.r = cv2.split(self.src)
		#_,self.g_bin=cv2.threshold(self.g,127,255,cv2.THRESH_BINARY)
		#_,self.r_bin=cv2.threshold(self.r,127,255,cv2.THRESH_BINARY)
		return(self.mask,self.g,self.r)