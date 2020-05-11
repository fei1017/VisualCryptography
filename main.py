import cv2
from encrypt import encrypt

## main
secret = cv2.imread('secret_image/secret.png',0)
encrypt(secret)