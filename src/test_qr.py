import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image
import zbarlight
import imutils

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    ret_val, img = cam.read()

    piece_set = set()

    for angle in np.arange(0, 180, 15):

        # rotate image
        rotated = imutils.rotate(img, angle)

        codes = pyzbar.decode(Image.fromarray(rotated))#, symbols=[pyzbar.ZBarSymbol.QRCODE])
        print("\ngot codes\n", "\n".join([str(c) for c in codes]))

        for c in codes:
            cv2.rectangle(rotated, (c.polygon[0].x, c.polygon[0].y), (c.polygon[2].x, c.polygon[2].y), (255, 0, 0), 2)

        piece_set = piece_set.union({c.data for c in codes})

        cv2.imshow("test", rotated)
        cv2.waitKey(0)

    print("Got total pieces:", piece_set)

    cam.release()
    cv2.destroyAllWindows()
