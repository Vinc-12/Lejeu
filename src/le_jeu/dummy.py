import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from le_jeu.dodge_the_roar import init_game

if __name__ == '__main__':
    init_game()
    print("Dummy")