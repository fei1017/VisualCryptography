import cv2
import numpy as np
import math
import copy

black_tag = 1
white_tag = 0
black_pixel = 0
white_pixel = 255

M, N = 3,3

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

def gaussian(x, y):
    sigma = 1.9
    return math.exp(-1*((abs(x)+abs(y))**2)/(2*(sigma**2)))

def calc_energy(pattern,M,N):
    height,width = pattern.shape
    energy = np.zeros((height,width),np.float)
    for i in range(height):
        for j in range(width):
            for m in range(-1*math.floor(M/2),math.ceil(M/2)):
                for n in range(-1*math.floor(N/2),math.ceil(N/2)):
                    energy[i,j] += pattern[bound(i+m,height),bound(j+n,width)]*gaussian(m,n)
    return energy

def findTightestCluster(pattern,energy):
    energy = energy + pattern*10000 ## to ensure pattern[max_position] == black_tag
    result = np.where(energy == np.amax(energy))
    TightestCluster = (result[0][0],result[1][0])
    return TightestCluster

def removeTighestCluster(pattern,energy,position):
    pattern[position] = white_tag
    for i in range(-1*math.floor(M/2),math.ceil(M/2)):
        for j in range(-1*math.floor(N/2),math.ceil(N/2)):
            if out_of_bound(i+position[0],pattern.shape[0]) or out_of_bound(j+position[1],pattern.shape[1]):
                continue
            energy[i+position[0],j+position[1]] -= gaussian(i,j)
    return pattern,energy

def findLargestVoid(pattern,energy):
    energy = energy + pattern*10000
    result = np.where(energy == np.amin(energy))
    LargestVoid = (result[0][0],result[1][0])
    return LargestVoid

def findLargestVoid_wRegion(pattern,energy,secret,region):
    min = 99999
    for i in range(pattern.shape[0]):
        for j in range(pattern.shape[1]):
            if secret[i,j] == region and pattern[i,j] == white_tag:
                if energy[i,j] < min:
                    min = energy[i,j]
                    LargestVoid = (i,j)
    return LargestVoid

def removeLargestVoid(pattern,energy,position):
    pattern[position] = black_tag
    for i in range(-1*math.floor(M/2),math.ceil(M/2)):
        for j in range(-1*math.floor(N/2),math.ceil(N/2)):
            if out_of_bound(i+position[0],pattern.shape[0]) or out_of_bound(j+position[1],pattern.shape[1]):
                continue
            energy[i+position[0],j+position[1]] += gaussian(i,j)
    return pattern,energy

def void_and_cluster1(secret,pattern):
    height,width = pattern.shape
    energy = calc_energy(pattern,3,3)

    while(1):
        TightestCluster = findTightestCluster(pattern,energy)
        pattern,energy = removeTighestCluster(pattern,energy,TightestCluster)

        LargestVoid = findLargestVoid_wRegion(pattern,energy,secret,secret[TightestCluster])
        pattern,energy = removeLargestVoid(pattern,energy,LargestVoid)

        if LargestVoid == TightestCluster:
            break

    return pattern

    # idx = 0
    # while(1):
    #   max = 0
    #   min = 999
    #   max_position = (height,width)
    #   min_position = (height,width)
    #   for i in range(height):
    #       for j in range(width):
    #           if secret[i,j] == white_pixel and pattern[i,j] == black_tag:
    #               sum = 0
    #               for m in range(-1*math.floor(M/2),math.ceil(M/2)):
    #                   for n in range(-1*math.floor(N/2),math.ceil(N/2)):
    #                       sum += pattern[bound(i+m,height),bound(j+n,width)]*mask[m,n]
    #               if sum > max:
    #                   max = sum
    #                   max_position = (i,j)

    #   pattern[max_position] = white_tag
    #   for i in range(height):
    #       for j in range(width):
    #           if secret[i,j] == white_pixel and pattern[i,j] == white_tag:
    #               sum = 0
    #               for m in range(-1*math.floor(M/2),math.ceil(M/2)):
    #                   for n in range(-1*math.floor(N/2),math.ceil(N/2)):
    #                       sum += pattern[bound(i+m,height),bound(j+n,width)]*mask[m,n]
    #               if sum < min:
    #                   min = sum
    #                   min_position = (i,j)
    #   if min_position != max_position:
    #       pattern[min_position] = black_tag
    #   else:
    #       pattern[max_position] = white_tag
    #       break
    #   print(idx)
    #   idx+=1


def void_and_cluster2(pattern):
    pattern_backup = copy.deepcopy(pattern)
    height,width = pattern.shape
    dither_array = np.zeros((height,width),np.int64)
    energy = calc_energy(pattern,3,3)

    #phase1
    ones = np.sum(pattern)
    rank = ones - 1
    while(rank >= 0):
        TightestCluster = findTightestCluster(pattern,energy)
        pattern,energy = removeTighestCluster(pattern,energy,TightestCluster)

        dither_array[TightestCluster] = rank
        rank -= 1

    #phase 2 & 3
    pattern = copy.deepcopy(pattern_backup)
    ones = np.sum(pattern)
    rank = ones
    while(rank < height*width):
        LargestVoid = findLargestVoid(pattern,energy)
        pattern,energy = removeLargestVoid(pattern,energy,LargestVoid)

        dither_array[LargestVoid] = rank
        rank += 1

    dither_array = dither_array/(np.max(dither_array))*255 #normalized

    return dither_array.astype('uint8')
