import cv2
import numpy as np
from pyzbar import pyzbar
import zbarlight
import imutils
import time

def find_qr_codes(img):
    codes = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
    print("\ngot codes\n", "\n".join([str(c) for c in codes]))

    return codes

def draw_rectangles(img, codes):
    for c in codes:
        cv2.rectangle(img, (c.polygon[0].x, c.polygon[0].y), (c.polygon[2].x, c.polygon[2].y), (255, 0, 0), 2)

def search_rotated():
    piece_set = set()

    for angle in np.arange(0, 180, 7.5):

        # rotate image
        rotated = imutils.rotate_bound(img, angle)

        codes = find_qr_codes(rotated)
        draw_rectangles(rotated, codes)

        piece_set = piece_set.union({c.data for c in codes})

        # cv2.imshow("test", rotated)
        # cv2.waitKey(0)

    print("Got total pieces:", piece_set)

if __name__ == '__main__':

    t = time.time()
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    ret_val, img = cam.read()
    e = time.time()
    print("time to take photo:", e - t)

    tmp_im_path = '/tmp/img.jpg'
    cv2.imwrite(tmp_im_path, img)

    codes = find_qr_codes(img)
    q = time.time()
    print("time to find qr codes:", q - e)
    print("total time to read", q - t)
    draw_rectangles(img, codes)
    r = time.time()
    print("time to find draw rectangles:", r - q)
    cv2.imshow("test", img)
    cv2.waitKey(0)

    cam.release()
    cv2.destroyAllWindows()
