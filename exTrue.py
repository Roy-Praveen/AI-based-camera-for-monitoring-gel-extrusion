from split import split
from geometries import geometries
from measurements import measurements
import cv2 
import numpy as np
import math


def exTrue(measure_frame):
	sp = split(measure_frame)
	img=sp.resize()
	'''cv2.imshow("OG IMAGE",img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''
	_,g_bin,r_bin = sp.split_binary()
	'''cv2.imshow("Needle Green",g_bin)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imshow("Gel Red",r_bin)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''


	##########################################################################
	#Introduction of filling-up option of segments with patches is required

	edged_g = cv2.Canny(g_bin, 30, 200)
	'''cv2.imshow("Border Green",edged_g)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''

	edged_r = cv2.Canny(r_bin, 30, 200)
	'''cv2.imshow("Border Red",edged_r)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''

	#########################################################################

	geo_g = geometries(g_bin)
	skel_g=geo_g.skeleton()
	g_larg_skel=geo_g.largest_skeleton_contour(skel_g)
	cp_edged_g=edged_g.copy()
	cp_edged_g2=edged_g.copy()
	cv2.drawContours(cp_edged_g, g_larg_skel, -1, 255, 3)
	'''cv2.imshow("edged_g",cp_edged_g)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''

	M = cv2.moments(g_larg_skel)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	#print(r_larg_skel)
	mp=np.array([cX, cY])
	mp=np.array([mp])
	mp=np.array([mp])
	r_larg_skel=np.concatenate((g_larg_skel, mp), axis=0)
	mp_g=(cX,cY)

	geo_r = geometries(r_bin)
	skel_r=geo_r.skeleton()
	r_larg_skel=geo_r.largest_skeleton_contour(skel_r)
	cp_edged_r=edged_r.copy()
	cp_edged_r2=edged_r.copy()
	cv2.drawContours(cp_edged_r, r_larg_skel, -1, 255, 3)
	'''cv2.imshow("edged_r",cp_edged_r)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''

	M = cv2.moments(r_larg_skel)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	#print(r_larg_skel)
	mp=np.array([cX, cY])
	mp=np.array([mp])
	mp=np.array([mp])
	r_larg_skel=np.concatenate((r_larg_skel, mp), axis=0)
	mp_r=(cX,cY)

	cv2.drawContours(cp_edged_r2, r_larg_skel, -1, 255, 3)
	'''cv2.imshow("ContourDraw",cp_edged_r2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''
	



	cv2.circle(cp_edged_r2, (cX, cY), 7, (255, 255, 255), -1)
	'''cv2.imshow("edged_center",cp_edged_r2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''

	#######################################################################

	mea = measurements(g_larg_skel,r_larg_skel,img,mp_g,mp_r)
	mea.merge_lines()
	angle_diff=mea.angle()
	print("Angle between Strut and Needle is ",angle_diff[0][0])

	#######################################################################

	(inter_x,inter_y)=mea.intersect()
	inter_point=(inter_x,inter_y)

	(g_skp,r_skp) = mea.skeleton_points()

	g_skp=(g_skp[0],g_skp[1])

	r_skp=(r_skp[0],r_skp[1])


	#######################################################################

	g_nor=mea.draw_normals('green',g_skp,inter_point)
	blk_1=np.zeros_like(edged_g)
	cv2.line(blk_1,g_nor[0],g_nor[1],255,1)
	ed_g=edged_g.copy()
	cv2.line(ed_g,g_nor[0],g_nor[1],255,1)
	
	'''cv2.imshow("Green Normal",ed_g)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''
	

	sub=cv2.subtract(edged_g,blk_1)
	sub=cv2.subtract(edged_g,sub)
	p1,p2 = cv2.findNonZero(sub)
	p = cv2.findNonZero(sub)
	pt=(p[0][0][0],p[0][0][1])
	pt=(pt[0],pt[1])
	pb=(p[-1][0][0],p[-1][0][1])
	pb=(pb[0],pb[1])
	ned_wid=math.dist(pt, pb)
	print("Width of Needle is",ned_wid)

	#######################################################################

	r_nor=mea.draw_normals('red',r_skp,inter_point)
	blk_1=np.zeros_like(edged_g)
	cv2.line(blk_1,r_nor[0],r_nor[1],255,1)
	ed_r=edged_r.copy()
	cv2.line(ed_r,r_nor[0],r_nor[1],255,1)
	
	'''cv2.imshow("Red Normal",ed_r)
	cv2.waitKey(0)
	cv2.destroyAllWindows()'''
	

	sub=cv2.subtract(edged_r,blk_1)
	sub=cv2.subtract(edged_r,sub)
	p = cv2.findNonZero(sub)
	pt=(p[0][0][0],p[0][0][1])
	pt=(pt[0],pt[1])
	pb=(p[-1][0][0],p[-1][0][1])
	pb=(pb[0],pb[1])
	gma=0
	gel_wid=math.dist(pt, pb)+gma
	print("Width of the strut is",gel_wid)
	###################################################################
	percent=((gel_wid-ned_wid)/ned_wid)*100
	return(percent)
