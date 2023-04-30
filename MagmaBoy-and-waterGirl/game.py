import sys
import pygame
from pygame.locals import *


class Game:
    def __init__(self):
        WINDOW_SIZE = (640, 480)
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Magma Boy and Hydro Girl")

        CHUNK_SIZE = 16
        DISPLAY_SIZE = (34 * CHUNK_SIZE, 25 * CHUNK_SIZE)
        self.display = pygame.Surface(DISPLAY_SIZE)

    def draw_level_screen(self, level_select):
        self.display.blit(level_select.screen, (0, 0))

        for level in range(2):
            image = level_select.titles[level + 1]
            title_x = (self.display.get_width() - image.get_width()) / 2
            title_y = 50 * level + 100
            self.display.blit(image, (title_x, title_y))

        left_cords = (50, 150)
        right_cords = (430, 150)
        self.display.blit(level_select.left_player, left_cords)
        self.display.blit(level_select.right_player, right_cords)

    def user_select_level(self, level_select, controller):
        
        level_index = 0
        level_dict = {
            0: "level1",
            1: "level2"
        }
        while True:
            self.draw_level_screen(level_select)
            events = pygame.event.get()
            if controller.press_key(events, K_DOWN):
                level_index += 1
                if level_index == 2:
                    level_index = 0
            if controller.press_key(events, K_UP):
                level_index -= 1
                if level_index == -1:
                    level_index = 1
            self.draw_level_select_indicator(level_select, level_index)

            if controller.press_key(events, K_RETURN):
                return level_dict[level_index]

    def draw_level_select_indicator(self, level_select, level_index):
        indicator = level_select.indicator_image
        location_x = (self.display.get_width() - indicator.get_width()) / 2
        location_y = level_index * 50 + 96
        indicator_location = (location_x, location_y)
        self.display.blit(level_select.indicator_image, indicator_location)
        self.refresh_window()

    def refresh_window(self):
        new_window_size, center_cords = self.adjust_scale()
        new_disp = pygame.transform.scale(self.display, new_window_size)
        self.screen.blit(new_disp, center_cords)
        pygame.display.update()

    def adjust_scale(self):
        window_size = self.screen.get_size()

        if window_size[0] / window_size[1] >= 1.5:
            display_size = (int(1.5 * window_size[1]), window_size[1])
        else:
            display_size = (window_size[0], int(.75 * window_size[0]))
        cords = ((window_size[0] - display_size[0]) / 2,
                 (window_size[1] - display_size[1]) / 2)

        return display_size, cords


    def draw_level_background(self, board):
        self.display.blit(board.get_background(), (0, 0))

    def draw_board(self, board):
        board_textures = board.get_board_textures()
        for y, row in enumerate(board.get_game_map()):
            for x, tile in enumerate(row):
                if tile != "0":
                    self.display.blit(
                        board_textures[f"{tile}"], (x * 16, y * 16)
                    )

    def draw_gates(self, gates):
        for gate in gates:
            self.display.blit(gate.gate_image, gate.gate_location)

            for location in gate.plate_locations:
                self.display.blit(gate.plate_image, location)

    def draw_doors(self, doors):
        for door in doors:
            self.display.blit(door.door_background, door.background_location)
            self.display.blit(door.door_image, door.door_location)
            self.display.blit(door.frame_image, door.frame_location)

    def draw_player(self, players):
        for player in players:
            if player.moving_right:
                player_image = player.side_image
            elif player.moving_left:
                player_image = pygame.transform.flip(
                    player.side_image, True, False)
            else:
                player_image = player.image
            player_image.set_colorkey((255, 0, 255))
            self.display.blit(player_image, (player.rect.x, player.rect.y))

    def move_player(self, board, gates, players):
        for player in players:
            player.calc_movement()
            movement = player.get_movement()

            collide_blocks = board.get_solid_blocks()
            for gate in gates:
                collide_blocks += gate.get_solid_blocks()

            collision_types = {
                'top': False,
                'bottom': False,
                'right': False,
                'left': False}

            player.rect.x += movement[0]
            hit_list = self.collision_test(player.rect, collide_blocks)
            for tile in hit_list:
                if movement[0] > 0:
                    player.rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    player.rect.left = tile.right
                    collision_types['left'] = True

            player.rect.y += movement[1]
            hit_list = self.collision_test(player.rect, collide_blocks)
            for tile in hit_list:
                if movement[1] > 0:
                    player.rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    player.rect.top = tile.bottom
                    collision_types['top'] = True

            if collision_types['bottom']:
                player.y_velocity = 0
                player.air_timer = 0
            else:
                player.air_timer += 1

            if collision_types['top']:
                player.y_velocity = 0

    def check_for_death(self, board, players):
        for player in players:
            if player.get_type() == "water":
                is_killed = self.collision_test(
                    player.rect, board.get_lava_pools())
            if player.get_type() == "magma":
                is_killed = self.collision_test(
                    player.rect, board.get_water_pools())
            is_killed += self.collision_test(player.rect, board.get_goo_pools())

            if is_killed:
                player.kill_player()

    def check_for_gate_press(self, gates, players):
        for gate in gates:
            plate_collisions = []
            for player in players:
                plates = gate.get_plates()
                plate_collisions += self.collision_test(player.rect, plates)
            if plate_collisions:
                gate.plate_is_pressed = True
            else:
                gate.plate_is_pressed = False
            gate.try_open_gate()

    def check_for_door_open(self, door, player):
        door_collision = self.collision_test(player.rect, [door.get_door()])
        if door_collision:
            door.player_at_door = True
        else:
            door.player_at_door = False
        door.try_raise_door()

    @staticmethod
    def level_is_done(doors):
        is_win = True
        for door in doors:
            if not door.is_door_open():
                is_win = False
        return is_win

    @staticmethod
    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
