import sys
import pygame
from pygame.locals import *


class Gates:
    def __init__(self, gate_location, plate_locatons):
        self.gate_location = gate_location
        self.plate_locations = plate_locatons
        self.plate_is_pressed = False
        self._gate_is_open = False

        self.load_images()
        self.make_rects()

    def load_images(self):
        self.gate_image = pygame.image.load('data/gates_and_plates/gate.png')
        self.gate_image.set_colorkey((255, 0, 255))
        self.plate_image = pygame.image.load('data/gates_and_plates/plate.png')
        self.plate_image.set_colorkey((255, 0, 255))

    def make_rects(self):
        x_cord = self.gate_location[0]
        y_cord = self.gate_location[1]
        self._gate = pygame.Rect(x_cord, y_cord, self.gate_image.get_width(),
                                 self.gate_image.get_height())

        self._plates = []
        for location in self.plate_locations:
            self._plates.append(
                pygame.Rect(location[0], location[1],
                            self.plate_image.get_width(),
                            self.plate_image.get_height()))

    def try_open_gate(self):
        CHUNK_SIZE = 16
        gate_x = self.gate_location[0]
        gate_y = self.gate_location[1]
        if self.plate_is_pressed and not self._gate_is_open:
            self.gate_location = (gate_x, gate_y - 2 * CHUNK_SIZE)
            self._gate.y -= 2 * CHUNK_SIZE
            self._gate_is_open = True
        if not self.plate_is_pressed and self._gate_is_open:
            self.gate_location = (gate_x, gate_y + 2 * CHUNK_SIZE)
            self._gate.y += 2 * CHUNK_SIZE
            self._gate_is_open = False

    def get_solid_blocks(self):
        return [self._gate]

    def get_plates(self):
        return self._plates
