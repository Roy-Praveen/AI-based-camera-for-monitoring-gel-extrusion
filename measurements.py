import numpy as np
import cv2
from skimage.transform import (hough_line, hough_line_peaks)
import math
import shapely
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt
import random

class measurements:
	def __init__(self,g_larg_skel,r_larg_skel,img,mp_g,mp_r):
		self.g_larg_skel=g_larg_skel
		self.r_larg_skel=r_larg_skel
		self.img=img
		self.mp_g=mp_g
		self.mp_r=mp_r
		self.mask = np.zeros_like(self.img)
		self.empty_mask = np.zeros_like(self.img)		

	def merge_lines(self):
		self.g_vec,self.g_cor=self.extend_skeleton(self.g_larg_skel,self.mp_g)
		self.g_point=(self.mask.shape[1]-1,self.righty),(0,self.lefty)
		self.r_vec,self.r_cor=self.extend_skeleton(self.r_larg_skel,self.mp_r)
		self.r_point=(self.mask.shape[1]-1,self.righty),(0,self.lefty)

	def extend_skeleton(self,largest_skeleton_contour,mp):
		self.largest_skeleton_contour=largest_skeleton_contour
		self.mp=mp
		[self.vx,self.vy,_,_] = cv2.fitLine(self.largest_skeleton_contour,cv2.DIST_L2,0,0.01,0.01)
		self.x,self.y=self.mp
		self.lefty = int((-self.x*self.vy/self.vx) + self.y)
		self.righty = int(((self.img.shape[1]-self.x)*self.vy/self.vx)+self.y)	

		cv2.line(self.img,(self.img.shape[1]-1,self.righty),(0,self.lefty),255,2)
		'''cv2.imshow('Bisectors',self.img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()'''
		return(np.array([self.vx,self.vy]),np.array([self.x,self.y]))

	def angle(self):
		gendpnt1=int(self.g_cor[0])
		gendpnt2=int(self.g_cor[1])
		corodinateimage=cv2.line(self.img,(0,0),(gendpnt1,gendpnt2),(0,0,255),3)
		rendpnt1=int(self.r_cor[0])
		rendpnt2=int(self.r_cor[1])
		corodinateimage=cv2.line(self.img,(0,0),(rendpnt1,rendpnt2),(0,0,255),3)
		gvendpnt1=int(self.g_vec[0][0])
		gvendpnt2=int(self.g_vec[1][0])
		corodinateimage=cv2.line(self.img,(0,0),(gvendpnt1,gvendpnt2),(0,0,255),3)
		rvendpnt1=int(self.r_vec[0][0])
		rvendpnt2=int(self.r_vec[1][0])
		corodinateimage=cv2.line(self.img,(0,0),(rvendpnt1,rvendpnt2),(0,0,255),3)

		'''cv2.imshow("coordinate image",corodinateimage)
		cv2.waitKey(0)
		cv2.destroyAllWindows()'''
		self.dot_product = np.dot(self.g_vec.T, self.r_vec)
		self.angle_2_x   = np.rad2deg(np.arccos(self.dot_product))
		return(self.angle_2_x)

	def intersect(self):
		self.line1 = LineString(self.r_point)
		self.line2 = LineString(self.g_point)
		self.int_pt = self.line1.intersection(self.line2)
		self.point_of_intersection = self.int_pt.x, self.int_pt.y
		'''
		print(self.int_pt.x)
		print(self.int_pt.y)
		intpointx= int(self.int_pt.x)
		intpointy= int(self.int_pt.y)
		
		corodinateimage=cv2.line(self.img,(0,0),(intpointx,intpointy),(0,255,0),3)
		
		cv2.imshow("Plus Intersection",corodinateimage)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		'''
		
		return(self.point_of_intersection)
	
	def skeleton_points(self):
		return(self.g_cor,self.r_cor)

	def draw_normals(self,flag,cor1,cor2):
		self.flag=flag
		if self.flag=='green':
			self.p1=np.array(cor1)
			self.p2=np.array(cor2)
			#self.mp12 = (self.p1 + self.p2) / 2
			#self.mp12 = (self.p1 + self.mp12) / 2
			#self.mp12 = (self.p1 + self.mp12) / 2

			self.s12 = (self.p2[1] - self.p1[1]) / (self.p2[0] - self.p1[0])
			self.ps12 = - 1 / self.s12
			self.c12 = self.p1[1] - self.ps12 * self.p1[0]
			#self.xMin = min(self.p1[1], self.p2[1])
			#self.xMax = max(self.p1[1], self.p2[1])
			#self.xSeries = np.array([self.xMin, self.xMax])
			self.xSeries = np.array([0, 480])
			self.ySeries12 = self.ps12 * self.xSeries + self.c12
			self.p1_p=(int(self.xSeries[0]),int(self.ySeries12[0]))
			self.p2_p=(int(self.xSeries[1]),int(self.ySeries12[1]))
			return(self.p1_p,self.p2_p)

		else:
			self.p1=np.array(cor1)
			self.p2=np.array(cor2)
			#self.mp12 = (self.p1 + self.p2) / 2
			#self.mp12 = (self.p1 + self.mp12) / 2
			#self.mp12 = (self.p1 + self.mp12) / 2
			
			self.s12 = (self.p2[1] - self.p1[1]) / (self.p2[0] - self.p1[0])
			self.ps12 = - 1 / self.s12
			self.c12 = self.p1[1] - self.ps12 * self.p1[0]
			#self.xMin = min(self.p1[0], self.p2[0])
			#self.xMax = max(self.p1[0], self.p2[0])
			#self.xSeries = np.array([self.xMin, self.xMax])
			self.xSeries = np.array([0, 480])
			self.ySeries12 = self.ps12 * self.xSeries + self.c12
			self.p1_p=(int(self.xSeries[0]),int(self.ySeries12[0]))
			self.p2_p=(int(self.xSeries[1]),int(self.ySeries12[1]))
			return(self.p1_p,self.p2_p)
		
		

		





		
		







		