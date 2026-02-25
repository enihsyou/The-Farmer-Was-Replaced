# Reference: https://github.com/Flekay/The-Farmer-Was-Replaced/blob/main/Maze/Single%20Drone/Shared_Vector_Flow_Field.py
s = get_world_size()

INF_METRIC = 999999
DIRECTIONS = [North, East, South, West]
OPPOSITES = {
    North: South,
    South: North,
    East: West,
    West: East,
}
RELATIVE = {
    North: (0, 1),
    South: (0, -1),
    East: (1, 0),
    West: (-1, 0),
}


MULTIPLIER = 2 ** (num_unlocked(Unlocks.Mazes) - 1)
# 迷宫大小
MSIZE = 8
# 需要的 Weird_Substance 数量
COSTS = MSIZE * MULTIPLIER
# 能获得的 Gold 数量
GOLDS = MSIZE * COSTS


# Helper recursive function to find walls and treasure
def scan_maze(maze, back=None):
    walls = set()
    for dir in DIRECTIONS:
        if dir != back:
            if move(dir):
                dir_back = OPPOSITES[dir]
                scan_maze(maze, dir_back)
                move(dir_back)
            else:
                walls.add(dir)
    # 必定非空，免得后面存在性检测
    maze[get_pos_x(), get_pos_y()] = walls


# Helper to populate the flowfield
def plot_flow_field(maze, dist_to_base, path_to_base, base):
    # use two stacks to simulate a queue, because pop() is faster than pop(0)
    in_stack = []
    out_stack = [(base, dist_to_base[base])]

    while in_stack or out_stack:
        if not out_stack:
            out_stack = in_stack[::-1]
            in_stack = []
        pos, dist = out_stack.pop()
        for dir in DIRECTIONS:
            if dir in maze[pos]:
                continue
            new_pos = virtual_move(pos, dir)
            # take out distance remembered
            if new_pos in dist_to_base:
                dist_old = dist_to_base[new_pos]
            else:
                dist_old = INF_METRIC
            # compare to current optimal distance
            dist_new = dist + 1
            # update if better
            if dist_new < dist_old:
                dist_to_base[new_pos] = dist_new
                path_to_base[new_pos] = OPPOSITES[dir]
                in_stack.append((new_pos, dist_new))


# Helper to compute the path to a base
def find_path(path_to_base, start):
    movements = []
    pos = start
    dir = path_to_base[pos]
    while dir:
        movements.append(dir)
        pos = virtual_move(pos, dir)
        dir = path_to_base[pos]
    return movements


def virtual_move(pos, direction):
    px, py = pos
    dx, dy = RELATIVE[direction]
    return px + dx, py + dy


# Helper to look for missing walls
def update_maze(maze, dist_to_base, path_to_base):
    old_pos = (get_pos_x(), get_pos_y())
    changed = False
    for dir in list(maze[old_pos]):
        if can_move(dir):
            new_pos = virtual_move(old_pos, dir)
            # Remove both sides of the wall
            maze[old_pos].remove(dir)
            maze[new_pos].remove(OPPOSITES[dir])
            changed = True
            # Update the flowfield
            plot_flow_field(maze, dist_to_base, path_to_base, new_pos)
    if changed:
        plot_flow_field(maze, dist_to_base, path_to_base, old_pos)


# move to BASE
for _ in range(4):
    move(East)
    move(North)
plant(Entities.Bush)
use_item(Items.Weird_Substance, COSTS)

# Map the maze
maze = {}
base = (get_pos_x(), get_pos_y())
dist_to_base = {base: 0}
path_to_base = {base: None}
scan_maze(maze)
plot_flow_field(maze, dist_to_base, path_to_base, base)

for i in range(301):
    # Recycle treasure if it's here
    use_item(Items.Weird_Substance, COSTS)

    # Compute paths from drone and goal to base
    back_to_base = find_path(path_to_base, (get_pos_x(), get_pos_y()))
    base_to_gold = find_path(path_to_base, measure())

    # Cancel the final moves if they're the same
    while back_to_base and base_to_gold and back_to_base[-1] == base_to_gold[-1]:
        base_to_gold.pop()
        back_to_base.pop()

    if i % 5 != 0:
        # Only update map every 10 iterations to save time
        for step in back_to_base:
            move(step)
        for step in base_to_gold[::-1]:
            move(OPPOSITES[step])
    else:
        # Follow the drone path forward
        for step in back_to_base:
            move(step)
            update_maze(maze, dist_to_base, path_to_base)
        # Follow the goal path backward
        for step in base_to_gold[::-1]:
            move(OPPOSITES[step])
            update_maze(maze, dist_to_base, path_to_base)

harvest()
