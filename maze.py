from __builtins__ import quick_print
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


def wrapper3(fn, arg0, arg1, arg2):
    def wrapped():
        return fn(arg0, arg1, arg2)

    return wrapped


def scan_maze(maze, direction, can_spawn):
    if direction == None:
        backwards = None
    else:
        backwards = OPPOSITES[direction]
    if direction != None:
        move(direction)

    searchable = []
    for dir in DIRECTIONS:
        if dir != backwards and can_move(dir):
            searchable.append(dir)

    maze[get_pos_x(), get_pos_y()] = direction_options()
    if len(searchable) == 1:
        scan_maze(maze, searchable[0], can_spawn)
    elif len(searchable) >= 2:
        drones = []
        for dir in searchable:
            if can_spawn:
                work = wrapper3(scan_maze, {}, dir, False)
                fork = spawn_drone(work)
                if fork == None:
                    scan_maze(maze, dir, False)
                else:
                    drones.append(fork)
                    can_spawn = False
            else:
                scan_maze(maze, dir, can_spawn)
        for drone in drones:
            fork_return = wait_for(drone)
            for key in fork_return:
                maze[key] = fork_return[key]

    if backwards != None:
        move(backwards)

    return maze


def plot_flow_field(maze, dist_to_base, path_to_base, base):
    # use two stacks to simulate a queue, because pop() is faster than pop(0)
    in_stack = []
    out_stack = [(base, dist_to_base[base])]

    while in_stack or out_stack:
        if not out_stack:
            while in_stack:
                out_stack.append(in_stack.pop())
        old_pos, dist = out_stack.pop()
        options = maze[old_pos]
        for dir in options:
            if options[dir]:
                new_pos = virtual_move(old_pos, dir)
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


def find_path(maze, path_to_base, start):
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


def direction_options():
    moveables = {}
    for dir in DIRECTIONS:
        moveables[dir] = can_move(dir)
    return moveables


def update_maze(maze, dist_to_base, path_to_base):
    pos = (get_pos_x(), get_pos_y())
    options = maze[pos]
    for dir in DIRECTIONS:
        if options[dir]:
            continue
        if can_move(dir):
            options[dir] = True
            plot_flow_field(maze, dist_to_base, path_to_base, pos)
            plot_flow_field(maze, dist_to_base, path_to_base, virtual_move(pos, dir))


def drone_work():
    # 等待其他无人机到位
    while not can_harvest():
        continue
    harvest()
    while num_items(Items.Hay) != BEGIN_HAY:
        continue

    # 生成迷宫
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, COSTS)

    # 了解迷宫
    maze = scan_maze({}, None, True)
    base = (get_pos_x(), get_pos_y())
    dist_to_base = {base: 0}
    path_to_base = {base: None}
    plot_flow_field(maze, dist_to_base, path_to_base, base)

    for i in range(301):
        use_item(Items.Weird_Substance, COSTS)

        back_to_base = find_path(maze, path_to_base, (get_pos_x(), get_pos_y()))
        base_to_gold = find_path(maze, path_to_base, measure())

        while back_to_base and base_to_gold and back_to_base[-1] == base_to_gold[-1]:
            back_to_base.pop()
            base_to_gold.pop()

        if i % 10:
            for step in back_to_base:
                move(step)
            for step in base_to_gold[::-1]:
                move(OPPOSITES[step])
        else:
            for step in back_to_base:
                move(step)
                update_maze(maze, dist_to_base, path_to_base)
            for step in base_to_gold[::-1]:
                move(OPPOSITES[step])
                update_maze(maze, dist_to_base, path_to_base)

    harvest()


def spawn_drones_16(work):
    def move_do(side_length, d, do):
        def fn():
            for _ in range(side_length):
                move(d)
            do()

        return fn

    def spawn_drone_task1():
        forked2 = spawn_drone(move_do(16, East, work))
        forked1 = spawn_drone(move_do(8, East, work))
        forked3 = spawn_drone(move_do(8, West, work))
        work()
        wait_for(forked1)
        wait_for(forked2)
        wait_for(forked3)

    forked1 = spawn_drone(move_do(16, North, spawn_drone_task1))
    forked2 = spawn_drone(move_do(8, North, spawn_drone_task1))
    forked3 = spawn_drone(move_do(8, South, spawn_drone_task1))
    spawn_drone_task1()
    wait_for(forked1)
    wait_for(forked2)
    wait_for(forked3)


START_HAY = num_items(Items.Hay)
BEGIN_HAY = START_HAY + 512 * 16

for _ in range(4):
    move(East)
    move(North)
spawn_drones_16(drone_work)
