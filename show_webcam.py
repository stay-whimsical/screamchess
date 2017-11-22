import cv2

def show_webcam(mirror=False):
	cam = cv2.VideoCapture(0)
	while True:
		ret_val, img = cam.read()
		#chess_state = process_image(img)
		cv2.imshow('webcam', img)
		if cv2.waitKey(1) == 27:
			break

def main():
	show_webcam()

if __name__ == '__main__':
	main()
