from __builtins__ import Entities, get_entity_type, max_drones, num_drones, harvest

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

MULTIPLIER = 2 ** (num_unlocked(Unlocks.Mazes) - 1)
# 需要的 Weird_Substance 数量
COSTS = s * MULTIPLIER
# 能获得的 Gold 数量
GOLDS = s * s * MULTIPLIER


def drone_work():
    am_the_last_drone = num_drones() == max_drones()
    # Mapping information
    WALLS = {}
    BASE = (get_pos_x(), get_pos_y())

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
                if new_pos not in WALLS:
                    return
                # Remove both sides of the wall
                WALLS[old_pos].remove(dir)
                WALLS[new_pos].remove(OPPOSITES[dir])
                # Update the flowfield
                do_bfs(old_pos)
                do_bfs(new_pos)

    if am_the_last_drone:
        plant(Entities.Bush)
        use_item(Items.Weird_Substance, COSTS)
    else:
        while get_entity_type() == Entities.Grass:
            continue

    # Map the maze
    scan_maze()
    do_bfs(BASE)

    while num_items(Items.Gold) < 9863168:
        # Recycle treasure if it's here
        if get_entity_type() == Entities.Treasure:
            if not use_item(Items.Weird_Substance, COSTS):
                if get_entity_type() == Entities.Treasure:
                    harvest()
                    return

        # Compute paths from drone and goal to base
        goals = measure()
        if goals == None:
            return
        dpath = get_path_to_base((get_pos_x(), get_pos_y()))
        gpath = get_path_to_base(goals)

        # Cancel the final moves if they're the same
        while dpath and gpath and dpath[-1] == gpath[-1]:
            gpath.pop()
            dpath.pop()

        # Follow the drone path forward
        for step in dpath:
            if measure() != goals:
                break
            move_and_break_walls(step)
        # Follow the goal path backward
        for step in gpath[::-1]:
            if measure() != goals:
                break
            move_and_break_walls(OPPOSITES[step])


def spawn_drones_32(work):
    w, h = 4, 8

    def wrapper(fn, arg0):
        def wrapped():
            fn(arg0)

        return wrapped

    def move_do(side_length, d, do):
        def fn():
            for _ in range(side_length):
                move(d)
            do()

        return fn

    def spawn_drone_task1(face):
        forked = spawn_drone(move_do(h, face, spawn_drone_task2))
        spawn_drone_task2()
        wait_for(forked)

    def spawn_drone_task2():
        forked = spawn_drone(move_do(w, East, wrapper(spawn_drone_task3, East)))
        spawn_drone_task3(West)
        wait_for(forked)

    def spawn_drone_task3(face):
        for _ in range(3):
            spawn_drone(work)
            for _ in range(w):
                move(face)
        work()

    forked = spawn_drone(move_do(h, North, wrapper(spawn_drone_task1, North)))
    spawn_drone_task1(South)
    wait_for(forked)


clear()
# while num_items(Items.Gold) < 9863168:
move(North)
move(East)
spawn_drones_32(drone_work)
