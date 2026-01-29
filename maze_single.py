WORLD_SIZE = get_world_size()
WORLD_IS_EVEN = WORLD_SIZE % 2 == 0
HALF_WORLD_SIZE = WORLD_SIZE // 2

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


def adjecent_coordination(cell, direction):
    # 返回指定格子在指定方向上的邻居格子坐标，可能在地图外
    x, y = cell
    dx, dy = OFFSETS[direction]
    return (x + dx, y + dy)


def harvest_golds():
    relocate_treasure()
    walls = set()
    explore_unkown_dfs(walls)

    while num_items(Items.Gold) < 614400:
        if get_entity_type() == Entities.Treasure:
            relocate_treasure()
        if explore_known_astar(walls):
            continue
        if explore_unkown_dfs(walls):
            continue
    harvest()


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
    pos = get_pos_x(), get_pos_y()
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
                adj = adjecent_coordination((get_pos_x(), get_pos_y()), dir)
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


def is_in_map(position):
    x, y = position
    return 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE


def shorest_navigation_maze(walls, start, target):
    # a* search 返回从 start 到 apple 的最短路径的移动指令列表
    def h(cell):
        ax, ay = cell
        tx, ty = target
        dx = abs(ax - tx)
        dy = abs(ay - ty)
        return dx + dy

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

    visited = set()
    visited.add(start)
    enqueue(start, 0)
    while queue_keys:
        current = dequeue()
        if current == target:
            return reconstruct_navigation(came_from, target)

        current_score = get_metric(g_score, current)
        cost_to_adj = current_score + 1
        for direction in DIRECTIONS:
            if (current, direction) in walls:
                continue
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


def explore_known_astar(walls):
    treasure = measure()
    current = get_pos_x(), get_pos_y()
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

harvest_golds()
