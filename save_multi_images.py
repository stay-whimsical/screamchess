import cv2

BACKTICK = 96

def one_frame(id=0, num=0):
  cam = cv2.VideoCapture(id)
  ret_val, img = cam.read()
  print("width: " + str(cam.get(3)))
  print("height: " + str(cam.get(4)))
  cv2.imwrite("testimage" + str(num) + ".png", img)

one_frame()
