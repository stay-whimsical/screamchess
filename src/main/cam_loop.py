from camera import board_image_processor as bip
import cv2
def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        #chess_state = process_image(img)
        cv2.imshow('webcam', img)
        if cv2.waitKey(1) == 27:
            break
            
          
 
def one_frame(id=0):
   cam = cv2.VideoCapture(id)
   ret_val, img = cam.read()
   #print("width: " + str(cam.get(3)))
   #print("height: " + str(cam.get(4)))
   # cv2.imwrite("testimage3.png", img)
   return img



def main():
    board_processor = bip.BoardProcessor(debug_image_mode=False)
    state = board_processor.get_cur_state()
    while True:
        img = one_frame()
        board_processor.update_state(img)
        ret_state = board_processor.get_cur_state()
        if ret_state != state:
            print 'Got state change, new state = '
            for row in ret_state:
                print row
            state = ret_state
    # show_webcam()

if __name__ == '__main__':
    main()
