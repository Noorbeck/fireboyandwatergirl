from board import Board
from gates import Gates
from character import HydroGirl
import pytest

import sys
import pygame
from pygame.locals import *

from game import Game
from doors import FireDoor, WaterDoor
from controller import ArrowsController, WASDController, GeneralController
from level_select import LevelSelect


magma_boy = pygame.Rect(16, 350, 16, 32)
hydro_girl = pygame.Rect(16, 350, 16, 32)

magma_boy_goo = pygame.Rect(272, 80, 16, 32)
hydro_girl_goo = pygame.Rect(272, 80, 16, 32)

magma_boy_lava = pygame.Rect(19 * 16, 23 * 16, 16, 32)
hydro_girl_lava = pygame.Rect(19 * 16, 23 * 16, 16, 32)

magma_boy_water = pygame.Rect(11 * 16, 23 * 16, 16, 32)
hydro_girl_water = pygame.Rect(11 * 16, 23 * 16, 16, 32)

magma_boy_gates = pygame.Rect(285, 128, 16, 32)
hydro_girl_gates = pygame.Rect(285, 128, 16, 32)

magma_boy_fired = pygame.Rect(64, 48, 16, 32)
hydro_girl_fired = pygame.Rect(64, 48, 16, 32)

magma_boy_waterd = pygame.Rect(128, 48, 16, 32)
hydro_girl_waterd = pygame.Rect(128, 48, 16, 32)


collision_cases = [

    (magma_boy, [], []),
    (hydro_girl, [], []),

    (magma_boy, [pygame.Rect(16, 350, 16, 16)], [pygame.Rect(16, 350, 16, 16)]),
    (hydro_girl, [pygame.Rect(16, 350, 16, 16)],
     [pygame.Rect(16, 350, 16, 16)]),

    (magma_boy_goo, [pygame.Rect(272, 80, 16, 16)],
     [pygame.Rect(272, 80, 16, 16)]),
    (hydro_girl_goo, [pygame.Rect(272, 80, 16, 16)],
     [pygame.Rect(272, 80, 16, 16)]),

    (magma_boy_lava, [pygame.Rect(19 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(19 * 16, 23 * 16, 16, 16)]),
    (hydro_girl_lava, [pygame.Rect(19 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(19 * 16, 23 * 16, 16, 16)]),

    (magma_boy_water, [pygame.Rect(11 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(11 * 16, 23 * 16, 16, 16)]),
    (hydro_girl_water, [pygame.Rect(11 * 16, 23 * 16, 16, 16)],
     [pygame.Rect(11 * 16, 23 * 16, 16, 16)]),

    (magma_boy_gates, [pygame.Rect(285, 128, 16, 16)],
     [pygame.Rect(285, 128, 16, 16)]),
    (hydro_girl_gates, [pygame.Rect(285, 128, 16, 16)],
     [pygame.Rect(285, 128, 16, 16)]),

    (magma_boy_fired, [pygame.Rect(64, 48, 16, 16)],
     [pygame.Rect(64, 48, 16, 16)]),
    (hydro_girl_fired, [pygame.Rect(64, 48, 16, 16)],
     [pygame.Rect(64, 48, 16, 16)]),

    (magma_boy_waterd, [pygame.Rect(128, 48, 16, 16)],
     [pygame.Rect(128, 48, 16, 16)]),
    (hydro_girl_waterd, [pygame.Rect(128, 48, 16, 16)],
     [pygame.Rect(128, 48, 16, 16)]),
]





@pytest.mark.parametrize("player,tile,hit_list", collision_cases)
def test_collision(player, tile, hit_list):
    assert Game.collision_test(player, tile) == hit_list






fire_door = FireDoor((64, 48))
water_door = WaterDoor((128, 48))


fire_door_both = FireDoor((16, 350))
fire_door_both._door_open = True
water_door_both = WaterDoor((16, 350))
water_door_both._door_open = True


fire_door_magma = FireDoor((16, 350))
fire_door_magma._door_open = True
water_door_magma = WaterDoor((128, 48))


fire_door_hydro = FireDoor((64, 48))
water_door_hydro = WaterDoor((16, 350))
water_door_hydro._door_open = True

level_done_cases = [

    ([fire_door, water_door], False),

    ([fire_door_both, water_door_both], True),


    ([fire_door_magma, water_door_magma], False),

    ([fire_door_hydro, water_door_hydro], False),
]


@pytest.mark.parametrize("doors, win_status", level_done_cases)
def test_level_is_done(doors, win_status):
    assert Game.level_is_done(doors) == win_status





motion_test_cases = [

    (True, False, False, True, False, False),

    (False, True, False, False, True, False),

    (False, False, True, False, False, True),

    (True, False, True, True, False, True),

    (False, True, True, False, True, True),
]


@pytest.mark.parametrize("moving_right, moving_left, jumping, \
                         moved_right, moved_left, jumped", motion_test_cases)
def test_movement(moving_right, moving_left, jumping,
                  moved_right, moved_left, jumped):

    controller = GeneralController()
    player_cords = (32, 336)
    player = HydroGirl(player_cords)

    gates = Gates((285, 128), [(190, 168), (390, 168)])
    board = Board('data/level1.txt')


    init_x = player.rect.x
    init_y = player.rect.y


    player.moving_right = moving_right
    player.moving_left = moving_left
    player.jumping = jumping

    Game.move_player(Game(), board, [gates], [player])

    assert (player.rect.x > init_x) == moved_right
    assert (player.rect.x < init_x) == moved_left
    assert (player.rect.y < init_y) == jumped
