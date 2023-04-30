import sys
import pygame
from pygame.locals import *

from game import Game
from board import Board
from character import MagmaBoy, HydroGirl
from controller import ArrowsController, WASDController, GeneralController
from gates import Gates
from doors import FireDoor, WaterDoor
from level_select import LevelSelect


def main():
    pygame.init()
    controller = GeneralController()
    game = Game()
    show_level_screen(game, controller)

def show_level_screen(game, controller):
    level_select = LevelSelect()
    level = game.user_select_level(level_select, controller)
    run_game(game, controller, level)


def show_win_screen(game, controller):
    win_screen = pygame.image.load('data/screens/win_screen.png')
    win_screen.set_colorkey((255, 0, 255))
    game.display.blit(win_screen, (0, 0))

    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_death_screen(game, controller, level):
    death_screen = pygame.image.load('data/screens/death_screen.png')
    death_screen.set_colorkey((255, 0, 255))
    game.display.blit(death_screen, (0, 0))
    while True:
        game.refresh_window()
        events = pygame.event.get()
        if controller.press_key(events, K_RETURN):
            run_game(game, controller, level)
        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)


def run_game(game, controller, level="level1"):
    is_paused = False
    if level == "level1":
        board = Board('data/level1.txt')
        gate_location = (285, 128)
        plate_locations = [(190, 168), (390, 168)]
        gate = Gates(gate_location, plate_locations)
        gates = [gate]

        fire_door_location = (64, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (128, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)

    if level == "level2":
        board = Board('data/level2.txt')
        gates = []

        fire_door_location = (390, 48)
        fire_door = FireDoor(fire_door_location)
        water_door_location = (330, 48)
        water_door = WaterDoor(water_door_location)
        doors = [fire_door, water_door]

        magma_boy_location = (16, 336)
        magma_boy = MagmaBoy(magma_boy_location)
        hydro_girl_location = (35, 336)
        hydro_girl = HydroGirl(hydro_girl_location)
        
    arrows_controller = ArrowsController()
    wasd_controller = WASDController()

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        events = pygame.event.get()
        
        if controller.press_key(events, K_f):
            is_paused = not is_paused

        if is_paused:
            game.display.blit(pause_screen, (0, 0))
            game.refresh_window()
            continue

        game.draw_level_background(board)
        game.draw_board(board)
        if gates:
            game.draw_gates(gates)
        game.draw_doors(doors)

        game.draw_player([magma_boy, hydro_girl])

        arrows_controller.control_player(events, magma_boy)
        wasd_controller.control_player(events, hydro_girl)

        game.move_player(board, gates, [magma_boy, hydro_girl])

        game.check_for_death(board, [magma_boy, hydro_girl])

        game.check_for_gate_press(gates, [magma_boy, hydro_girl])

        game.check_for_door_open(fire_door, magma_boy)
        game.check_for_door_open(water_door, hydro_girl)

        game.refresh_window()

        if hydro_girl.is_dead() or magma_boy.is_dead():
            show_death_screen(game, controller, level)

        if game.level_is_done(doors):
            show_win_screen(game, controller)

        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()
