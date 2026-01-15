
WORLD_SIZE = get_world_size()
WORLD_IS_EVEN = WORLD_SIZE % 2 == 0
HALF_WORLD_SIZE = WORLD_SIZE // 2

INF_METRIC = 999999

OPPOSITES = {
    North: South,
    South: North,
    East: West,
    West: East,
}

DIRECTIONS = [North, East, South, West]


def is_even(n):
    return (n % 2) == 0


def is_odd(n):
    return (n % 2) == 1


def random_int(max):
    return random() * max // 1


def random_choice(array):
    return array[random_int(len(array))]


def array_filter(fn, array):
    after = []
    for item in array:
        if fn(item):
            after.append(item)
    return after


def current_position():
    return (get_pos_x(), get_pos_y())


zeroing_position = (0, 0)


def is_in_map(position):
    x, y = position
    return 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE


def distance_1d_flat(start, end):
    # 平直空间两个点的距离
    return abs(end - start)


def distance_1d_torus(start, end):
    # 环空间两个点的距离
    d = distance_1d_flat(start, end)
    return min(d, WORLD_SIZE - d)


def calc_distance_2d(start, end, fn_1d):
    start_x, start_y = start
    end_x, end_y = end
    return fn_1d(start_x, end_x) + fn_1d(start_y, end_y)


def distance_2d_flat(start, end):
    # 平直空间两个点的曼哈顿距离
    return calc_distance_2d(start, end, distance_1d_flat)


def distance_2d_torus(start, end):
    # 环空间两个点的曼哈顿距离
    return calc_distance_2d(start, end, distance_1d_torus)


def make_boundary_2d(bottomleft, w, h):
    # 构造一个矩形边界
    bx, by = bottomleft
    return (bottomleft, (bx + w, by + h))


def walk_straight(direction, steps):
    # 朝 direction 方向走 steps 步
    for _ in range(steps):
        move(direction)


def move_1d_flat(start, end, forward):
    # 在平直世界中沿一维轴线移动到位置 end
    backward = False
    if end < start:
        # 逻辑假定正向前进，如果位置反了就调转方向
        backward = True
    steps = distance_1d_flat(start, end)
    if backward:
        walk_straight(OPPOSITES[forward], steps)
    else:
        walk_straight(forward, steps)


def move_2d_flat(position):
    # 在平直的一维轴线移动到位置
    cx, cy = current_position()
    tx, ty = position
    move_1d_flat(cx, tx, East)
    move_1d_flat(cy, ty, North)


def move_1d_torus(start, end, forward):
    # 在环世界中沿一维轴线移动到位置 end
    backward = False
    if end < start:
        # 逻辑假定正向前进，如果位置反了就调转方向
        backward = True
    if distance_1d_flat(start, end) > HALF_WORLD_SIZE:
        # 跨越边界更近
        backward = not backward
    steps = distance_1d_torus(start, end)
    if backward:
        walk_straight(OPPOSITES[forward], steps)
    else:
        walk_straight(forward, steps)


def move_2d_torus(position):
    # 在环世界中移动到点 (x, y)
    cx, cy = current_position()
    tx, ty = position
    move_1d_torus(cx, tx, East)
    move_1d_torus(cy, ty, North)


def move_2d_random_neighbor(boundary):
    # 随机移动到当前格子的一个邻居格子
    bottomleft, topright = boundary
    bx, by = bottomleft
    tx, ty = topright
    cx, cy = current_position()
    possiblities = []
    if cx + 1 <= tx:
        possiblities.append(East)
    if cx - 1 >= bx:
        possiblities.append(West)
    if cy + 1 <= ty:
        possiblities.append(North)
    if cy - 1 >= by:
        possiblities.append(South)
    move(possiblities[random_int(len(possiblities))])


def move_2d_random(boundary):
    # 随机移动到范围内的某个格子
    bottomleft, topright = boundary
    bx, by = bottomleft
    tx, ty = topright
    rx = random_int(tx - bx + 1) + bx
    ry = random_int(ty - by + 1) + by
    move_2d_torus((rx, ry))


def adjecent_coordination(cell, direction):
    # 返回指定格子在指定方向上的邻居格子坐标，可能在地图外
    x, y = cell
    if direction == North:
        return (x, y + 1)
    if direction == South:
        return (x, y - 1)
    if direction == East:
        return (x + 1, y)
    if direction == West:
        return (x - 1, y)


def routing_nearest(cells):
    # 从格子列表中生成一条路径
    # 每次都走向列表中离自己最近的格子
    cells = cells[:]  # 复制一份以免修改原列表
    route = []
    start = current_position()
    while cells:
        mindex = indexof_nearest(start, cells)
        mvalue = cells.pop(mindex)
        route.append(mvalue)
        start = mvalue
    return route


def indexof_nearest(start, cells):
    # 在位置列表中离指定位置最近的格子索引
    def distance_fn(cell):
        return distance_2d_torus(start, cell)

    mindex = indexof_minimal(distance_fn, cells)
    return mindex


def iterate_cell_inorder(fn, cells):
    # 从当前位置开始以给定顺序访问指定的格子列表
    for cell in cells:
        move_2d_torus(cell)
        fn()


def traverse_rectangle(fn, w, h):
    # 从当前位置开始访问一个矩形区域的每个格子
    if w == 1:
        start_point = current_position()
        traverse_rectangle_s_shape(fn, h, North, 1, None)
        move_2d_torus(start_point)
        return
    if h == 1:
        start_point = current_position()
        traverse_rectangle_s_shape(fn, w, East, 1, None)
        move_2d_torus(start_point)
        return
    if is_even(w):
        # 第一行用于折返
        move(North)
        traverse_rectangle_s_shape(fn, h - 1, North, w, East)
        move(South)
        traverse_rectangle_s_shape(fn, w, West, 1, None)
        return
    if is_even(h):
        # 第一列用于折返
        move(East)
        traverse_rectangle_s_shape(fn, w - 1, East, h, South)
        move(West)
        traverse_rectangle_s_shape(fn, h, North, 1, None)
        return

    # 棋盘染色奇偶性校验无法回到起点，那就结束在离起点最近的位置，距离等于 2
    traverse_rectangle_s_shape(fn, h, North, 1, None)
    move(East)
    traverse_rectangle_s_shape(fn, w - 1, East, h - 2, South)
    move(South)
    traverse_rectangle_s_shape(fn, 2, South, w - 1, West)
    # 再挪回到起始点
    move(West)
    move(South)


def traverse_rectangle_s_shape(fn, w, x, h, y):
    # 从当前位置开始以 U 形顺序访问矩形区域的每个格子
    # x 决定一开始沿哪个方向前进, w 决定前进距离
    # y 决定曲线延伸的方向, h 决定前进距离
    for i in range(1, h + 1):
        if is_odd(i):
            backforth = x
        else:
            backforth = OPPOSITES[x]
        for j in range(1, w + 1):
            fn()
            if j == w:
                break
            move(backforth)
        if i == h:
            break
        move(y)


def hamiltonian_navigation():
    # 在整个地图上以哈密顿路径覆盖所有点的的移动指令列表
    directions = []
    move = directions.append

    def traverse_rectangle_s_shape(w, x, h, y):
        # 和同名函数实现相同，只是记录移动指令
        for i in range(1, h + 1):
            if is_odd(i):
                backforth = x
            else:
                backforth = OPPOSITES[x]
            for j in range(1, w + 1):
                if j == w:
                    break
                move(backforth)
            if i == h:
                break
            move(y)

    # 世界一定是偶数尺寸
    move(North)
    traverse_rectangle_s_shape(WORLD_SIZE - 1, North, WORLD_SIZE, East)
    move(South)
    traverse_rectangle_s_shape(WORLD_SIZE, West, 1, None)
    return directions


def indexof_minimal(fn, items):
    # 从 items 中选出 fn(item) 最小的 index
    min_index = 0
    min_value = fn(items[0])
    for idx in range(1, len(items)):
        item = items[idx]
        value = fn(item)
        if value < min_value:
            min_value = value
            min_index = idx
    return min_index


def convert_to_heap(array, cmp_fn):
    # 将数组原地转换为堆结构
    n = len(array)
    for i in range((n - 2) // 2, -1, -1):
        heapify_down(array, cmp_fn, i, n - 1)


def append_to_heap(heap, cmp_fn, item):
    heap.append(item)
    heapify_up(heap, cmp_fn, len(heap) - 1)


def pop_from_heap(heap, cmp_fn):
    n = len(heap)
    heap[0], heap[n - 1] = heap[n - 1], heap[0]
    item = heap.pop()
    heapify_down(heap, cmp_fn, 0, n - 1)
    return item


def peek_from_heap(heap):
    return heap[0]


def heapify_down(heap, cmp_fn, top, end):
    while True:
        left = 2 * top + 1
        if left >= end:
            break
        to_cmp, right = left, left + 1
        if right < end and cmp_fn(heap[right], heap[left]):
            to_cmp = right
        if cmp_fn(heap[top], heap[to_cmp]):
            break
        heap[top], heap[to_cmp] = heap[to_cmp], heap[top]
        top = to_cmp


def heapify_up(heap, cmp_fn, idx):
    while idx > 0:
        parent = (idx - 1) // 2
        if cmp_fn(heap[parent], heap[idx]):
            break
        heap[idx], heap[parent] = heap[parent], heap[idx]
        idx = parent


def heap_sort(array, cmp_fn):
    n = len(array)
    heap = convert_to_heap(array, cmp_fn)
    sort = []
    for _ in range(n):
        sort.append(pop_from_heap(heap, cmp_fn))
    return sort


def reverse_list(l):
    for i in range(len(l) // 2):
        j = len(l) - 1 - i
        l[i], l[j] = l[j], l[i]


def metric_of_inf():
    graph = []
    for _ in range(WORLD_SIZE):
        col = []
        for _ in range(WORLD_SIZE):
            col.append(INF_METRIC)
        graph.append(col)
    return graph


def get_metric(metric, cell):
    x, y = cell
    return metric[x][y]


def set_metric(metric, cell, value):
    x, y = cell
    metric[x][y] = value


def reconstruct_direction(start, end):
    # 要求两个相邻
    sx, sy = start
    ex, ey = end
    if sx == ex:
        if sy > ey:
            return South
        if sy < ey:
            return North
    if sy == ey:
        if sx < ex:
            return East
        if sx > ex:
            return West


def reconstruct_navigation(came_from, target):
    navigations = []
    cell = target
    while cell in came_from:
        cell_parent = came_from[cell]
        direction = reconstruct_direction(cell_parent, cell)
        navigations.append(direction)
        cell = cell_parent
    reverse_list(navigations)
    return navigations


def shorest_navigation(blocks, start, target):
    # a* search 返回从 start 到 apple 的最短路径的移动指令列表
    def h(cell):
        return distance_2d_flat(cell, target)

    came_from = {}
    g_score = metric_of_inf()
    set_metric(g_score, start, 0)
    f_score = metric_of_inf()
    set_metric(f_score, start, h(start))

    queue_keys = []
    queue_data = {}

    def enqueue(cell, priority):
        if priority in queue_keys:
            queue_data[priority].append(cell)
        else:
            queue_keys.append(priority)
            queue_data[priority] = [cell]

    def dequeue():
        min_priority = min(queue_keys)
        min_cells = queue_data[min_priority]
        if len(min_cells) == 1:
            queue_keys.remove(min_priority)
        return min_cells.pop()

    visited = set(blocks)
    visited.add(start)
    enqueue(start, 0)
    while queue_keys:
        current = dequeue()
        if current == target:
            return reconstruct_navigation(came_from, target)

        current_score = get_metric(g_score, current)
        cost_to_adj = current_score + 1
        for direction in DIRECTIONS:
            adj = adjecent_coordination(current, direction)
            if not is_in_map(adj):
                continue
            if adj in visited:
                continue
            visited.add(adj)
            if cost_to_adj < get_metric(g_score, adj):
                came_from[adj] = current
                set_metric(g_score, adj, cost_to_adj)
                set_metric(f_score, adj, cost_to_adj + h(adj))
                enqueue(adj, get_metric(f_score, adj))

    return []

def safe_spawn_drone(task):
    drone = spawn_drone(task)
    if drone == None:
        return task()
    return wait_for(drone)

if __name__ == "__main__":
    clear()
    points = [
        (11,1),
    ]
    for p in points:
        start = (6, 1)
        block = [(8,1),(7,1),(6,1)]
        move_2d_flat(start)
        a = get_tick_count()
        path = shorest_navigation(block, start, p)
        b = get_tick_count()
        for d in path:
            move(d)
        print(current_position() == p, b - a)
