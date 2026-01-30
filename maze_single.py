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
OFFSETS = {
    North: (0, 1),
    South: (0, -1),
    East: (1, 0),
    West: (-1, 0),
}


AMOUNT = s * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
BASE = (s // 2, s // 2)


# Mapping information
WALLS = {}


# Helper recursive function to find walls and treasure
def scan_maze(back=None):
    walls = set()
    for dir in DIRECTIONS:
        if dir != back:
            if move(dir):
                dir_back = OPPOSITES[dir]
                scan_maze(dir_back)
                move(dir_back)
            else:
                walls.add(dir)
    # 必定非空，免得后面存在性检测
    WALLS[get_pos_x(), get_pos_y()] = walls


DIST_TO_BASE = {BASE: 0}
DIRS_TO_BASE = {BASE: None}


# Helper to populate the flowfield
def do_bfs(pos):
    x, y = pos

    # use two stacks to simulate a queue, because pop() is faster than pop(0)
    in_stack = []
    out_stack = [(x, y, DIST_TO_BASE[x, y])]

    def enqueue(item):
        in_stack.append(item)

    def dequeue():
        if not out_stack:
            while in_stack:
                out_stack.append(in_stack.pop())
        return out_stack.pop()

    while in_stack or out_stack:
        old_x, old_y, dist = dequeue()
        for dir in DIRECTIONS:
            if dir in WALLS[old_x, old_y]:
                continue
            dx, dy = OFFSETS[dir]
            nx, ny = old_x + dx, old_y + dy
            new_pos = (nx, ny)
            # take out distance remembered
            if new_pos in DIST_TO_BASE:
                dist_old = DIST_TO_BASE[new_pos]
            else:
                dist_old = INF_METRIC
            # compare to current optimal distance
            dist_new = dist + 1
            # update if better
            if dist_new < dist_old:
                DIST_TO_BASE[new_pos] = dist_new
                DIRS_TO_BASE[new_pos] = OPPOSITES[dir]
                enqueue((nx, ny, dist_new))


# Helper to compute the path to a base
def get_path_to_base(pos):
    path = []
    x, y = pos
    dir = DIRS_TO_BASE[x, y]
    while dir:
        path.append(dir)
        dx, dy = OFFSETS[dir]
        x, y = x + dx, y + dy
        dir = DIRS_TO_BASE[x, y]
    return path


# Helper to look for missing walls
def move_and_break_walls(step):
    move(step)
    old_pos = (get_pos_x(), get_pos_y())
    for dir in list(WALLS[old_pos]):
        if can_move(dir):
            ox, oy = old_pos
            dx, dy = OFFSETS[dir]
            new_pos = (ox + dx, oy + dy)
            # Remove both sides of the wall
            WALLS[old_pos].remove(dir)
            WALLS[new_pos].remove(OPPOSITES[dir])
            # Update the flowfield
            do_bfs(old_pos)
            do_bfs(new_pos)


# move to BASE
for _ in range(s // 2):
    move(East)
    move(North)
plant(Entities.Bush)
use_item(Items.Weird_Substance, AMOUNT)

# Map the maze
scan_maze()
do_bfs(BASE)

for i in range(601):
    # Compute paths from drone and goal to base
    dpath = get_path_to_base((get_pos_x(), get_pos_y()))
    gpath = get_path_to_base(measure())

    # Recycle treasure if it's here
    use_item(Items.Weird_Substance, AMOUNT)

    # Cancel the final moves if they're the same
    while dpath and gpath and dpath[-1] == gpath[-1]:
        gpath.pop()
        dpath.pop()
    if i % 10 != 0:
        # Only update map every 10 iterations to save time
        for step in dpath:
            move(step)
        for stop in gpath[::-1]:
            move(OPPOSITES[stop])
    else:
        # Follow the drone path forward
        for step in dpath:
            move_and_break_walls(step)
        # Follow the goal path backward
        for step in gpath[::-1]:
            move_and_break_walls(OPPOSITES[step])
harvest()
