# -*- coding: utf-8 -*-
"""
Toplevel module. Says hi to the dev, listens for keystrokes to test interface,
prints state as necessary. Instructions roughly correspond to ACTIONS.md, and
are usually implemented in other modules in the package.
"""
import sys
from collections import namedtuple
from events import Events
from time import sleep
import logging
import threading
import random

import gamestate
import camera
import media


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
EVENTS = Events()


def print_welcome():
    welcome = u"""
  ██████  ▄████▄   ██▀███  ▓█████ ▄▄▄       ███▄ ▄███▓    ▄████▄   ██░ ██ ▓█████   ██████   ██████
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀▒████▄    ▓██▒▀█▀ ██▒   ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██    ▒ ▒██    ▒
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒███  ▒██  ▀█▄  ▓██    ▓██░   ▒▓█    ▄ ▒██▀▀██░▒███   ░ ▓██▄   ░ ▓██▄
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██ ▒██    ▒██    ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄   ▒   ██▒  ▒   ██▒
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒░▒████▒▓█   ▓██▒▒██▒   ░██▒   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒██████▒▒▒██████▒▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░▒▒   ▓▒█░░ ▒░   ░  ░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░ ░ ░  ░ ▒   ▒▒ ░░  ░      ░     ░  ▒    ▒ ░▒░ ░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░
░  ░  ░  ░          ░░   ░    ░    ░   ▒   ░      ░      ░         ░  ░░ ░   ░   ░  ░  ░  ░  ░  ░
      ░  ░ ░         ░        ░  ░     ░  ░       ░      ░ ░       ░  ░  ░   ░  ░      ░        ░
         ░                                               ░
                                          by Karbloraide

Instructions:
"""
    print(welcome)
    print_directions()


def print_directions():
    for instruction in INSTRUCTIONS:
        print('  {} - {} - {}\n'.format(instruction.keystroke,
                                        instruction.name,
                                        instruction.description))
    print('Until I can look up something better, remember to Ctrl-D to send the newline. Python rules')


def quit(state, events):
    events.quit()
    return gamestate.Gamestate(current_game=state.current_game, should_go_on=False)


def reset_state(state, events):
    events.reset()
    return gamestate.fresh_gamestate()


def print_state(state, events):
    print('board=\n{}'.format(str(state.current_game)))
    print('should_go_on={}'.format(state.should_go_on))
    return state


MIN_EVERLOOP_SECONDS = 10
MAX_EVERLOOP_SECONDS = 45


def everloop(state, events):
    """
    A function that we're adding out of SHEER DESPERATION AND DOWNSCOPEYNESS!
    This takes the MIN and MAX number of seconds defined above and play a random
    sound on them, forever!
    """
    t = threading.Thread(target=_loop_and_play_randoms, args=())
    log.debug('STARTING EVERLOOP')
    t.start()
    return state


def stop_everloop(state, events):
    global shouldLoop
    shouldLoop = False
    return state


def _loop_and_play_randoms():
    global shouldLoop
    global MIN_EVERLOOP_SECONDS
    global MAX_EVERLOOP_SECONDS
    shouldLoop = True
    while shouldLoop:
        num_seconds = random.randint(MIN_EVERLOOP_SECONDS, MAX_EVERLOOP_SECONDS)
        log.debug('{} seconds until the next sound!'.format(num_seconds))
        sleep(num_seconds)
        media.test_sound(None, None)


Instruction = namedtuple('Instruction', 'keystroke name description function')


INSTRUCTIONS = [
    Instruction(
        keystroke='s',
        name='Start',
        description='Start the event loop.',
        function=camera.start_event_loop),
    Instruction(
        keystroke='S',
        name='Stop',
        description='Stop the event loop.',
        function=camera.stop_event_loop),
    Instruction(
        keystroke='p',
        name='Print',
        description='Print the current game state.',
        function=print_state),
    Instruction(
        keystroke='N',
        name='New Game (or reset)',
        description='Discards the current game, replaces it with a new one.',
        function=reset_state),
    Instruction(
        keystroke='n',
        name='Advance move',
        description='',
        function=None),
    Instruction(
        keystroke='t',
        name='Test sound',
        description='Play a sound for me!',
        function=media.test_sound),
    Instruction(
        keystroke='T',
        name='Test sound sequence',
        description='Play sounds, multiple!',
        function=media.test_sound_sequence),
    Instruction(
        keystroke='L',
        name='EVERLOOP',
        description='Play sounds within a random interval, forever!',
        function=everloop),
    Instruction(
        keystroke='l',
        name='stop EVERLOOP',
        description='Make the everlooping stop!',
        function=stop_everloop),
    Instruction(
        keystroke='q',
        name='Quit',
        description='Quit the Python process.',
        function=quit)
]


def on_press(char, state):
    """
    Listen for a key on release, determine what to do.
    """
    for instruction in INSTRUCTIONS:
        if char == instruction.keystroke:
            return instruction.function(state, EVENTS)
    print('I don\'t understand, please try again!')
    return state


def listen_for_keystrokes():
    state = gamestate.fresh_gamestate()
    print('Give me a command: ')
    while True:
        char = sys.stdin.read(1)
        if char != '\n':
            print('Command: ')
            new_state = on_press(char, state)
            if not new_state.should_go_on:
                break
            state = new_state


def on_camera_start():
    print('Got an event!')


def receive_new_image(msg):
    print(msg)

EVENTS.start_camera += on_camera_start
EVENTS.new_image += receive_new_image


if __name__ == '__main__':
    print_welcome()
    listen_for_keystrokes()
