# -*- coding: utf-8 -*-
"""
Toplevel module. Says hi to the dev, listens for keystrokes to test interface,
prints state as necessary. Instructions roughly correspond to ACTIONS.md, and
are usually implemented in other modules in the package.
"""
import sys
from collections import namedtuple
from events import Events

import gamestate
import camera

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
                                          by Karblora

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
    print(state)
    return state


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
    while True:
        print('Give me a command: ')
        char = sys.stdin.read(1)
        if char != '\n':
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
