from __builtins__ import Entities, change_hat, get_entity_type, measure
from library import *


def harvest_dianosaus():
    # https://github.com/chuyangliu/snake
    hamiltonian_route = hamiltonian_navigation()
    hamiltonian_index = {}
    phantom_drone = (0, 0)
    for i in range(len(hamiltonian_route)):
        hamiltonian_index[phantom_drone] = i
        phantom_drone = adjecent_coordination(phantom_drone, hamiltonian_route[i])

    move_2d_flat((0, 0))
    change_hat(Hats.Dinosaur_Hat)
    stuck = False
    snake = [current_position()]  # tail to head
    while not stuck:
        if get_entity_type() == Entities.Apple:
            apple = measure()
        head = current_position()
        consider_shortcut = len(snake) < 2 * WORLD_SIZE
        if consider_shortcut:
            path = shorest_navigation(snake, head, apple)
        else:
            path = [hamiltonian_route[hamiltonian_index[head]]]
        if not path:
            stuck = True
            break
        for dir in path:
            move_away_from_apple = get_entity_type() == Entities.Apple
            if not move(dir):
                stuck = True
                break
            if consider_shortcut:
                snake.append(current_position())
                if not move_away_from_apple:
                    snake.pop(0)
    change_hat(Hats.Brown_Hat)


def harvest_dianosaus_pathfinding():
    change_hat(Hats.Dinosaur_Hat)
    stuck = False
    snake = [current_position()]
    while not stuck:
        apple = measure()
        head = current_position()
        path = shorest_navigation(snake, head, apple)
        if not path:
            stuck = True
            break
        for dir in path:
            move_away_from_apple = get_entity_type() == Entities.Apple
            if not move(dir):
                stuck = True
                break
            snake.append(current_position())
            if not move_away_from_apple:
                snake.pop(0)
    change_hat(Hats.Brown_Hat)

print(__name__)
if __name__ == "__main__":
    while True:
        harvest_dianosaus()
