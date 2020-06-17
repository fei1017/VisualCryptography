import cv2
import numpy as np
import random
import math
from vac import void_and_cluster1, void_and_cluster2

black_tag = 1
white_tag = 0
black_pixel = 0
white_pixel = 255

M, N = 3,3

# def halftoning(image):
# 	##now only binarizing
# 	height,width = image.shape
# 	resultImage = np.zeros((height,width),np.uint8)
# 	for i in range(height):
# 		for j in range(width):
# 			if image[i,j] >= 128:
# 				resultImage[i,j] = white_pixel
# 			else:
# 				resultImage[i,j] = black_pixel
# 	return resultImage

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
			if rn < 0.5:
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

def join(image1,image2):
	if image1.shape != image2.shape:
		print("join error")
		exit(1)

	height,width = image1.shape
	resultImage = image1 ^ image2

	# for i in range(height):
	# 	for j in range(width):
	# 		resultImage[i,j] = (image1[i,j] ^ image2[i,j])
	return resultImage

def pattern_to_image(pattern):
	image = (1 - pattern) * 255
	return image

def image_to_pattern(image):
	pattern = 1 - (image/255)
	return pattern.astype('int')


def thres(image,dither_array):
	ah,aw = dither_array.shape
	h,w = image.shape
	for i in range(h):
		for j in range(w):
			if image[i,j] > dither_array[i%ah,j%aw]:
				image[i,j] = 255
			else:
				image[i,j] = 0
	return image


def encrypt(secret,share1,share2):
	# secret = halftoning(secret)
	# print(secret.shape)

	rp1,rp2 = generate_random_pattern(secret)

	cv2.imwrite('output/rp1.jpg',pattern_to_image(rp1))
	cv2.imwrite('output/rp2.jpg',pattern_to_image(rp2))

	join_rp = join(rp1,rp2)
	cv2.imwrite('output/join_rp.jpg',pattern_to_image(join_rp))

	sp1 = void_and_cluster1(secret,rp1)
	sp2 = void_and_cluster1(secret,rp2)

	cv2.imwrite('output/sp1.jpg',pattern_to_image(sp1))
	cv2.imwrite('output/sp2.jpg',pattern_to_image(sp2))

	join_sp = join(sp1,sp2)
	cv2.imwrite('output/join_sp.jpg',pattern_to_image(join_sp))

	dither_array1 = void_and_cluster2(sp1)
	dither_array2 = void_and_cluster2(sp2)

	cv2.imwrite('output/dither_array1.jpg',dither_array1)
	cv2.imwrite('output/dither_array2.jpg',dither_array2)
	# dither_array1 = cv2.imread('output/dither_array1.jpg',0)
	# dither_array2 = cv2.imread('output/dither_array2.jpg',0)

	# sh1 = cv2.imread('share1.jpg',0)
	# sh2 = cv2.imread('share2.jpg',0)
	# sh2 = resize(sh2,sh1.shape)

	enc1 = thres(share1,dither_array1)
	enc2 = thres(share2,dither_array2)

	cv2.imwrite('output/enc1.jpg',enc1)
	cv2.imwrite('output/enc2.jpg',enc2)	

	enc1 = cv2.imread('output/enc1.jpg',0)
	enc2 = cv2.imread('output/enc2.jpg',0)

	join_enc = join(image_to_pattern(enc1),image_to_pattern(enc2))
	cv2.imwrite('output/join_enc.jpg',pattern_to_image(join_enc))


