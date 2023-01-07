import pygame

from robingame.input.queue import InputQueue


class KeyboardInputQueue(InputQueue):
    def get_new_values(self) -> tuple[int]:
        scancode_wrapper = pygame.key.get_pressed()
        return tuple(scancode_wrapper[ii] for ii in range(len(scancode_wrapper)))
