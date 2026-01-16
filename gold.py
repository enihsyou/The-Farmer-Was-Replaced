from __builtins__ import max_drones, measure, num_drones, set_world_size, spawn_drone
from library import *


def harvest_golds():
    relocate_treasure()
    walls = set()
    explore_unkown_dfs(walls)

    while True:
        if get_entity_type() == Entities.Treasure:
            relocate_treasure()
            if num_drones() < max_drones():
                single_drone(walls)
        if explore_known_astar(walls):
            continue
        if explore_unkown_dfs(walls):
            continue

def single_drone(walls):
    treasure = measure()  # 下一轮再启动

    def new_drone():
        while measure() == treasure:
            pass
        while True:
            if get_entity_type() == Entities.Treasure:
                relocate_treasure()
                if num_drones() < max_drones():
                    single_drone(walls)
            if random() < 0.2:
                return # 有几率退出，取得新的 walls 变量
            if explore_known_astar(walls):
                continue
            if explore_unkown_dfs(walls):
                continue

    spawn_drone(new_drone)


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


def update_walls(walls):
    pos = current_position()
    for dir in DIRECTIONS:
        loc = (pos, dir)
        if can_move(dir):
            if loc in walls:
                walls.remove(loc)
        else:
            walls.add(loc)


def explore_unkown_dfs(walls):
    visited = set()  # 访问过的交叉点
    treasure = measure()

    def explore_direction(d):
        def f():
            moveable_dirs = [d]  # 记录可以前进的方向
            move_history = []  # 移动记录
            while len(moveable_dirs) == 1:
                dir = moveable_dirs[0]
                move(dir)
                move_history.append(dir)
                update_walls(walls)
                if get_entity_type() == Entities.Treasure:
                    return True
                if get_entity_type() != Entities.Hedge:
                    return True  # 说明程序已经结束
                moveable_dirs = moveable_directions(dir)
            for dir in moveable_dirs:
                adj = adjecent_coordination(current_position(), dir)
                if adj in visited:
                    continue
                visited.add(adj)
                task = explore_direction(dir)
                if task():
                    return True

            if measure() != treasure:
                return False

            for i in range(len(move_history) - 1, -1, -1):
                move(OPPOSITES[move_history[i]])

        return f

    if get_entity_type() == Entities.Treasure:
        relocate_treasure()
        return True

    for dir in DIRECTIONS:
        if can_move(dir):
            task = explore_direction(dir)
            if task():
                return True


def explore_known_astar(walls):
    treasure = measure()
    current = current_position()
    path = shorest_navigation_maze(walls, current, treasure)
    if path:
        c = 0
        for dir in path:
            if not move(dir):
                return False
            if measure() != treasure:
                return False
            update_walls(walls)
            c += 1
            if c % 100 == 99:
                single_drone(walls)
        return True
    return False


if __name__ == "__main__":
    set_world_size(12)
    harvest_golds()
