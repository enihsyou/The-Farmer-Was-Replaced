s = get_world_size()

INF_METRIC = 999999
DIRECTIONS = [North, East, South, West]
OPPOSITES = {
    North: South,
    South: North,
    East: West,
    West: East,
    None: None,
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


def wrapper2(fn, arg0, arg1):
    def wrapped():
        return fn(arg0, arg1)

    return wrapped


def scan_maze(maze, direction):
    backwards = OPPOSITES[direction]
    if direction != None:
        move(direction)

    searchable = []
    for dir in DIRECTIONS:
        if dir != backwards and can_move(dir):
            searchable.append(dir)

    maze[get_pos_x(), get_pos_y()] = direction_options()
    if len(searchable) == 1:
        scan_maze(maze, searchable[0])
    if len(searchable) >= 2:
        drones = []
        for dir in searchable:
            work = wrapper2(scan_maze, {}, dir)
            fork = spawn_drone(work)
            if fork == None:
                scan_maze(maze, dir)
            else:
                drones.append(fork)
        for drone in drones:
            fork_return = wait_for(drone)
            for key in fork_return:
                maze[key] = fork_return[key]

    if backwards != None:
        move(backwards)

    return maze


def find_path(maze, position, treasure, direction):
    backwards = OPPOSITES[direction]

    if direction != None:
        # 计算移动后的位置
        px, py = position
        dx, dy = RELATIVE[direction]
        position = px + dx, py + dy

    if position == treasure:
        # 刚好在宝藏上
        if direction == None:
            return []
        # 移动后在宝藏上
        return [direction]

    options = maze[position]
    for dir in DIRECTIONS:
        # 尝试每一个可移动的方向
        if dir == backwards or not options[dir]:
            continue
        path_rev = find_path(maze, position, treasure, dir)
        if path_rev:
            if direction != None:
                path_rev.append(direction)
            return path_rev


def direction_options():
    moveables = {}
    for dir in DIRECTIONS:
        moveables[dir] = can_move(dir)
    return moveables


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

    maze = scan_maze({}, None)
    took = 0
    while True:
        base = (get_pos_x(), get_pos_y())
        gold = measure()
        path = find_path(maze, base, gold, None)[::-1]

        scan = took % 10 == 0
        for step in path or []:
            move(step)
            # 每 N 轮更新地图寻找捷径
            # if scan:
            #     maze[get_pos_x(), get_pos_y()] = direction_options()

        use_item(Items.Weird_Substance, COSTS)
        took += 1
        if measure() == gold:
            # 300 次到头了
            harvest()
            return


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

clear()
move(North)
move(North)
move(North)
move(North)
move(East)
move(East)
move(East)
move(East)
spawn_drones_16(drone_work)
