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
    visited = set() # 访问过的交叉点

    def explore_direction(d):
        def f():
            moveable_dirs = [d] # 记录可以前进的方向
            move_history = [] # 移动记录
            while len(moveable_dirs) == 1:
                dir = moveable_dirs[0]
                move(dir)
                move_history.append(dir)
                if get_entity_type() == Entities.Treasure:
                    relocate_treasure()
                    return True
                if get_entity_type() != Entities.Hedge:
                    return True # 说明程序已经结束
                moveable_dirs = moveable_directions(dir)
            for dir in moveable_dirs:
                adj = adjecent_coordination(current_position(), dir)
                if adj in visited:
                    continue
                visited.add(adj)
                task = explore_direction(dir)
                if task():
                    return True

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


if __name__ == "__main__":
    while True:
        harvest_golds()
