import cv2
from encrypt import encrypt
import halftone

def resize(img, shape):
    return cv2.resize(img, (shape[1], shape[0]))

secret_path = 'secret_image/top_secret.jpg'
secrethalftone_path = 'secret_image/top_secret_halftoned.jpg'
share1_path = 'share1.jpg'
share2_path = 'share2.jpg'

secret = cv2.imread(secret_path,0)
secret = resize(secret, (400,600))

share1 = cv2.imread(share1_path,0)
share1 = resize(share1, (400,600))

share2 = cv2.imread(share2_path,0)
share2 = resize(share2, (400,600))

cv2.imwrite(secret_path,secret)
h = halftone.Halftone(secret_path)
h.make( sample = 2, scale = 5)

# main
secret = cv2.imread(secrethalftone_path,0)
encrypt(secret, share1, share2)
