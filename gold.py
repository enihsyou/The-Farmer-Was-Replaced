from __builtins__ import Entities, get_entity_type, get_ground_type
from library import *


def harvest_golds():
    relocate_treasure()
    explore_unkown_dfs()


def relocate_treasure():
    substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    if get_entity_type() != Entities.Treasure:
        plant(Entities.Bush)
    use_item(Items.Weird_Substance, substance)


def moveable_directions(come_from):
    dirs = []
    for dir in DIRECTIONS:
        if dir == OPPOSITES[come_from]:
            continue
        if can_move(dir):
            dirs.append(dir)
    return dirs


def explore_unkown_dfs():
    visited = set()

    def explore_direction(d):
        def f():
            moveable_dirs = [d]
            backtraces = [d]
            while len(moveable_dirs) == 1:
                dir = moveable_dirs[0]
                move(dir)
                backtraces.append(dir)
                visited.add(current_position())
                if get_entity_type() == Entities.Treasure:
                    relocate_treasure()
                    return
                if get_entity_type() != Entities.Hedge:
                    return  # 说明程序已经结束
                moveable_dirs = moveable_directions(dir)
            for dir in moveable_dirs:
                adj = adjecent_coordination(current_position(), dir)
                if adj in visited:
                    continue
                task = explore_direction(dir)
                if not spawn_drone(task):
                    task()

            for i in range(len(backtraces) - 1, -1, -1):
                move(OPPOSITES[backtraces[i]])
            return

        return f

    if get_entity_type() == Entities.Treasure:
        return harvest()

    for dir in DIRECTIONS:
        if can_move(dir):
            task = explore_direction(dir)
            if not spawn_drone(task):
                task()


if __name__ == "__main__":
    # clear()
    set_world_size(3)
    while True:
        harvest_golds()
    # while True:
