import cv2

BACKTICK = 96

def show_webcam(id=0):
  cam = cv2.VideoCapture(id)
  while True:
    ret_val, img = cam.read()
    cv2.imshow("my webcam oh god please", img)
    if cv2.waitKey(1) == BACKTICK:
      break
  cv2.destroyAllWindows()


show_webcam()
