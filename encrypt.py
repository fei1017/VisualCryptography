import cv2
import numpy as np
import random
import math

black_tag = 1
white_tag = 0
black_pixel = 0
white_pixel = 255

def resize(img, height=800):
    """ Resize image to given height """
    rat = height / img.shape[0]
    return cv2.resize(img, (int(rat * img.shape[1]), height))

def halftoning(image):
	##now only binarizing
	height,width = image.shape
	resultImage = np.zeros((height,width),np.uint8)
	for i in range(height):
		for j in range(width):
			if image[i,j] >= 128:
				resultImage[i,j] = white_pixel
			else:
				resultImage[i,j] = black_pixel
	return resultImage

def opposite(x):
	if x == black_tag:
		return white_tag
	elif x == white_tag:
		return black_tag

def generate_random_pattern(secret):
	height,width = secret.shape
	rp1 = np.zeros((height,width),np.uint8)
	rp2 = np.zeros((height,width),np.uint8)

	for i in range(height):
		for j in range(width):
			rn = random.random()
			if rn < 0.45:
				tag = black_tag
			else:
				tag = white_tag
			if secret[i,j] == black_pixel:
				rp1[i,j] = tag
				rp2[i,j] = opposite(tag)
			else:
				rp1[i,j] = tag
				rp2[i,j] = tag
	return rp1,rp2

# def join(image1,image2):
# 	if image1.shape != image2.shape:
# 		print("join error")
# 		exit(1)

# 	height,width = image1.shape
# 	resultImage = np.zeros((height,width),np.uint8)
# 	for i in range(height):
# 		for j in range(width):
# 			if image1[i,j] == image2[i,j]:
# 				resultImage[i,j] = white_tag
# 			else:
# 				resultImage[i,j] = black_tag
# 	return resultImage

def join(image1,image2):
	if image1.shape != image2.shape:
		print("join error")
		exit(1)

	height,width = image1.shape
	resultImage = np.zeros((height,width),np.uint8)
	for i in range(height):
		for j in range(width):
			if image1[i,j] + image2[i,j] > black_tag:
				resultImage[i,j] = black_tag
			else:
				resultImage[i,j] = image1[i,j] + image2[i,j]
	return resultImage

def pattern_to_image(pattern):
	height,width = pattern.shape
	image = np.zeros((height,width),np.uint8)
	for i in range(height):
		for j in range(width):
			if pattern[i,j] == black_tag:
				image[i,j] = black_pixel
			elif pattern[i,j] == white_tag:
				image[i,j] = white_pixel
	return image

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

def void_and_cluster(secret,pattern):
	M = 3
	N = 3
	def gaussian(x, y):
		sigma = 1.9
		if abs(m)+abs(n) > 13:
			return 0
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
					if abs(m)+abs(n) > 13:
						continue
					energy[i,j] += pattern[bound(i+m,height),bound(j+n,width)]*mask[m,n]

	idx = 0
	while(1):
		max = 0
		min = 999
		for i in range(height):
			for j in range(width):
				if pattern[i,j] == black_tag:
					if energy[i,j] > max:
						max = energy[i,j]
						max_position = (i,j)

		pattern[max_position] = white_tag
		centre = max_position
		for i in range(-1*math.floor(M/2),math.ceil(M/2)):
			for j in range(-1*math.floor(N/2),math.ceil(N/2)):
				if out_of_bound(i+centre[0],height) or out_of_bound(j+centre[1],width):
					continue
				if abs(i)+abs(j) > 13:
					continue
				energy[i+centre[0],j+centre[1]] -= mask[i,j]

		for i in range(height):
			for j in range(width):
				if secret[i,j] == secret[max_position] and pattern[i,j] == white_tag:
					if energy[i,j] < min:
						min = energy[i,j]
						min_position = (i,j)

		pattern[min_position] = black_tag
		if min_position == max_position:
			break

		#debug# 
		print(idx,min_position,max_position)
		idx+=1
		#debug#

		centre = min_position
		for i in range(-1*math.floor(M/2),math.ceil(M/2)):
			for j in range(-1*math.floor(N/2),math.ceil(N/2)):
				if out_of_bound(i+centre[0],height) or out_of_bound(j+centre[1],width):
					continue
				if abs(i)+abs(j) > 13:
					continue
				energy[i+centre[0],j+centre[1]] += mask[i,j]

	# idx = 0
	# while(1):
	# 	max = 0
	# 	min = 999
	# 	max_position = (height,width)
	# 	min_position = (height,width)
	# 	for i in range(height):
	# 		for j in range(width):
	# 			if secret[i,j] == white_pixel and pattern[i,j] == black_tag:
	# 				sum = 0
	# 				for m in range(-1*math.floor(M/2),math.ceil(M/2)):
	# 					for n in range(-1*math.floor(N/2),math.ceil(N/2)):
	# 						sum += pattern[bound(i+m,height),bound(j+n,width)]*mask[m,n]
	# 				if sum > max:
	# 					max = sum
	# 					max_position = (i,j)

	# 	pattern[max_position] = white_tag
	# 	for i in range(height):
	# 		for j in range(width):
	# 			if secret[i,j] == white_pixel and pattern[i,j] == white_tag:
	# 				sum = 0
	# 				for m in range(-1*math.floor(M/2),math.ceil(M/2)):
	# 					for n in range(-1*math.floor(N/2),math.ceil(N/2)):
	# 						sum += pattern[bound(i+m,height),bound(j+n,width)]*mask[m,n]
	# 				if sum < min:
	# 					min = sum
	# 					min_position = (i,j)
	# 	if min_position != max_position:
	# 		pattern[min_position] = black_tag
	# 	else:
	# 		pattern[max_position] = white_tag
	# 		break
	# 	print(idx)
	# 	idx+=1

	return pattern

def encrypt(secret):
	secret = halftoning(secret)
	print(secret.shape)

	rp1,rp2 = generate_random_pattern(secret)

	cv2.imwrite('output/rp1.jpg',pattern_to_image(rp1))
	cv2.imwrite('output/rp2.jpg',pattern_to_image(rp2))

	join_rp = join(rp1,rp2)
	cv2.imwrite('output/join_rp.jpg',pattern_to_image(join_rp))

	sp1 = void_and_cluster(secret,rp1)
	sp2 = void_and_cluster(secret,rp2)

	cv2.imwrite('output/sp1.jpg',pattern_to_image(sp1))
	cv2.imwrite('output/sp2.jpg',pattern_to_image(sp2))

	join_sp = join(rp1,rp2)
	cv2.imwrite('output/join_sp.jpg',pattern_to_image(join_sp))

	joinjoin = join(join_rp,join_sp)
	cv2.imwrite('output/joinjoin.jpg',pattern_to_image(joinjoin))
