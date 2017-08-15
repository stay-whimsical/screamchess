"""
Modules related to operating the camera to read a gamestate. Has a dependency on
chess to appropriately construct board instances.

That said, this drives the main event loop; it's up to this code to use the
camera to determine when a move has occurred and what it even was.
"""
import cv2
import threading
import logging

from gamestate import Gamestate

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
BACKTICK_ASCII = 96
SHOULD_SHOW_WEBCAM = True


def start_event_loop(state, events):
    """
    Turns on the camera (if off), start watching for events and subsequently
    sending them to the Mother Brain.
    """
    log.debug('Starting event loop!')
    events.start_camera()
    t = threading.Thread(target=_show_webcam, args=(events,))
    t.start()
    return Gamestate(current_game=state.current_game, should_go_on=True)


def stop_event_loop(state, events):
    """
    Turns off the camera (if on), stops sending events.
    """
    log.debug('Stopping event loop!')
    _stop_webcam(events)
    return Gamestate(current_game=state.current_game, should_go_on=True)


def _show_webcam(events, id=0):
    """
    Opens the webcam. Does so in a new thread so that we don't block the rest of
    the process.
    """
    global SHOULD_SHOW_WEBCAM
#    cam = cv2.VideoCapture(id)
    SHOULD_SHOW_WEBCAM = True
    while SHOULD_SHOW_WEBCAM:
#        ret_val, img = cam.read()
#        cv2.imshow("my webcam oh god please", img)
        img = "ell oh ell"
        log.debug("hi hi hi")
        events.new_image(img)


def _stop_webcam(events):
    global SHOULD_SHOW_WEBCAM
    SHOULD_SHOW_WEBCAM = False
    events.stop_camera()
    cv2.destroyAllWindows()
