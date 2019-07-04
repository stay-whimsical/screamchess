import cv2
import sys

if __name__ == '__main__':
    img_out = sys.argv[1]

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    ret_val, img = cam.read()

    print("writing to: ", img_out)
    cv2.imwrite(img_out, img)

    cv2.imshow("test", img)
    cv2.waitKey(0)
