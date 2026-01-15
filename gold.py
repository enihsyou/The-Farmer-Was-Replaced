from __builtins__ import get_entity_type, measure
from library import *


def harvest_golds():
    set_world_size(10)
    substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    move_2d_torus((1, 1))
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, substance)
    explore_unkown_dfs(set())



def explore_unkown_dfs(walls):
    if get_entity_type() == Entities.Treasure:
        return harvest()
    start = current_position()
    visited = {start}
    # 记录当前在哪个位置，能搜索哪些方向，无路可走了朝哪回退
    stack = [(list(DIRECTIONS), None)]
    while stack:
        directions, backtrace = stack[-1]
        if not directions:
            stack.pop()
            if backtrace:
                move(backtrace)
            continue
        dir = directions.pop()
        pos = current_position()
        if not can_move(dir):
            walls.add((pos, dir))
            continue  # 那个方向有墙
        adj = adjecent_coordination(pos, dir)
        if adj in visited:
            continue  # 那个方向去过了
        visited.add(adj)
        stack.append((list(DIRECTIONS), OPPOSITES[dir]))
        move(dir)  # 接下来探索那个方向
        if get_entity_type() == Entities.Treasure:
            return harvest()

    print("no route")  # 所有路径都探索过了没有路可走了
    return False



if __name__ == "__main__":
    clear()
    while True:
        harvest_golds()
