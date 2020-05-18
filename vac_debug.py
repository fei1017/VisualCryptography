import cv2
import numpy as np
import random
import math

black_tag = 1
white_tag = 0
black_pixel = 0
white_pixel = 255

height,width = 5,5
def pattern_to_image(pattern,scale):
	height,width = pattern.shape
	image = np.zeros((height*scale,width*scale),np.uint8)
	for i in range(height):
		for j in range(width):
			if pattern[i,j] == black_tag:
				assign = black_pixel
			elif pattern[i,j] == white_tag:
				assign = white_pixel
			ii = i*scale
			jj = j*scale
			for i_ in range(scale):
				for j_ in range(scale):
					image[ii+i_,jj+j_] = assign
	return image

def createPattern():
	pattern =  [[1,1,0,0,0,1],
				[0,0,1,1,0,0],
				[0,1,1,1,1,0],
				[1,0,1,0,1,1],
				[0,0,0,1,0,1]]
	return np.array(pattern)

def bound(x,X):
	if x < 0:
		return 0
	if x > X-1:
		return X-1
	return x

def out_of_bound(x,X):
	if x < 0 or x > X-1:
		return True
	return False

def show_pattern(pattern):

	cv2.imshow('pattern',pattern_to_image(pattern,40))
	cv2.waitKey(0)

def vac(pattern):
	M = 3
	N = 3
	def gaussian(x, y):
		sigma = 1.9
		return math.exp(-1*((abs(x)+abs(y))**2)/(2*(sigma**2)))

	mask = np.zeros((M,N),np.float)
	for m in range(-1*math.floor(M/2),math.ceil(M/2)):
		for n in range(-1*math.floor(N/2),math.ceil(N/2)):
			mask[m,n] = gaussian(m,n)

	height,width = pattern.shape
	energy = np.zeros((height,width),np.float)
	for i in range(height):
		for j in range(width):
			for m in range(-1*math.floor(M/2),math.ceil(M/2)):
				for n in range(-1*math.floor(N/2),math.ceil(N/2)):
					energy[i,j] += pattern[bound(i+m,height),bound(j+n,width)]*mask[m,n]

	while(1):
		max = 0
		min = 999
		for i in range(height):
			for j in range(width):
				if pattern[i,j] == black_tag:
					if energy[i,j] > max:
						max = energy[i,j]
						max_position = (i,j)

		print(energy)
		print('max pos = ' + str(max_position) + '\n')
		show_pattern(pattern)

		pattern[max_position] = white_tag
		centre = max_position
		for i in range(-1*math.floor(M/2),math.ceil(M/2)):
			for j in range(-1*math.floor(N/2),math.ceil(N/2)):
				if out_of_bound(i+centre[0],height) or out_of_bound(j+centre[1],width):
					continue
				energy[i+centre[0],j+centre[1]] -= mask[i,j]

		for i in range(height):
			for j in range(width):
				#if secret[i,j] == secret[max_position] and pattern[i,j] == white_tag:
				if pattern[i,j] == white_tag:
					if energy[i,j] < min:
						min = energy[i,j]
						min_position = (i,j)

		print(energy)
		print('min pos = ' + str(min_position) + '\n')
		show_pattern(pattern)

		pattern[min_position] = black_tag
		if min_position == max_position:
			break

		centre = min_position
		for i in range(-1*math.floor(M/2),math.ceil(M/2)):
			for j in range(-1*math.floor(N/2),math.ceil(N/2)):
				if out_of_bound(i+centre[0],height) or out_of_bound(j+centre[1],width):
					continue
				energy[i+centre[0],j+centre[1]] += mask[i,j]

pattern = createPattern()
cv2.imwrite('ori.jpg',pattern_to_image(pattern,40))
vac(pattern)

cv2.imshow('pattern',pattern_to_image(pattern,40))
cv2.waitKey(0)

cv2.imwrite('rslt.jpg',pattern_to_image(pattern,40))
cv2.imwrite('rslt_not.jpg',pattern_to_image(np.logical_not(pattern),40))