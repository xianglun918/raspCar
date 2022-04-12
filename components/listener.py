__author__ = 'xianglun918'

import keyboard


class KeyListener:
    def __init__(self, car):
        self.car = car
        self.set_mode()

    def set_mode(self):
        yes_list = ('y', 'yes')
        no_list = ('n', 'no')
        while True:
            choice = input('Do you want to initiate the keyboard input? [YES|no]')
            if choice.lower() in yes_list:
                print('You choose: yes ...')
                self.start_listening()
                break
            elif choice.lower() in no_list:
                print('You choose: no ...')
                break
            else:
                print("Invalid input, try again.")

    def start_listening(self):
        print('Start keyboard listening...')
        print('Press esc to release keyboard hook')
        keyboard.hook(self.event_trigger)

    def event_trigger(self, x):
        if x.name == 'esc':
            print('esc pressed...')
            keyboard.unhook_all()
        elif x.name == 'w' or x.name == 'up':
            self.car.move('forward')
        elif x.name == 's' or x.name == 'down':
            self.car.move('forward')
        elif x.name == 'a' or x.name == 'left':
            self.car.move('leftTurn')
        elif x.name == 'd' or x.name == 'right':
            self.car.move('forward')
