from __builtins__ import can_harvest
s = get_world_size()
N = 2000000000
W = 0.75

OFFSETS = {
    North: (0, 1),
    South: (0, -1),
    East: (1, 0),
    West: (-1, 0),
}
OPPOSITE = {
    North: South,
    South: North,
    East: West,
    West: East,
}


def visit_neighbors_creator(dirs):
    visited = set()

    def r(i):
        for d in dirs:
            cx, cy = get_pos_x(), get_pos_y()
            dx, dy = OFFSETS[d]
            nx, ny = cx + dx, cy + dy
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            move(d)
            plant(Entities.Bush)
            if i < 3:
                r(i + 1)
            # backtrack
            move(OPPOSITE[d])

    return r


VISIT_EAST = visit_neighbors_creator([East, North, South])
VISIT_WEST = visit_neighbors_creator([West, North, South])
VISIT_NORTH = visit_neighbors_creator([North])
VISIT_SOUTH = visit_neighbors_creator([South])


def plant_bush_around():
    move(West)
    VISIT_WEST(2)
    move(East)

    VISIT_NORTH(1)
    VISIT_SOUTH(1)

    move(East)

    VISIT_NORTH(1)
    VISIT_SOUTH(1)

    move(East)
    VISIT_EAST(2)
    move(West)


def harvest_poly_hay():
    while get_water() < W and num_items(Items.Water) > 32:
        use_item(Items.Water)
    if can_harvest():
        harvest()
        c, _ = get_companion()
        while c != Entities.Bush:
            harvest()
            c, _ = get_companion()
    return num_items(Items.Hay) < N


def work_drone_task():
    plant_bush_around()
    while True:
        if harvest_poly_hay():
            move(West)
        else:
            break
        if harvest_poly_hay():
            move(East)
        else:
            break


def diagonal_move_do(side_lenth, d1, d2, do):
    def fn():
        for _ in range(side_lenth):
            move(d1)
            move(d2)
        do()

    return fn


DIRS = [North, East, South, West]


def spawn_drone_task1():
    for i in range(len(DIRS)):
        d1 = DIRS[i]
        d2 = DIRS[(i + 1) % len(DIRS)]
        spawn_drone(diagonal_move_do(8, d1, d2, spawn_drone_task2(i)))
        spawn_drone(diagonal_move_do(4, d1, d1, work_drone_task))
    work_drone_task()


def spawn_drone_task2(d):
    def fn():
        for i in range(len(DIRS)):
            d1 = DIRS[i]
            d2 = DIRS[(i + 1) % len(DIRS)]
            spawn_drone(diagonal_move_do(4, d1, d2, spawn_drone_task3(i)))
        work_drone_task()

    return fn


def spawn_drone_task3(d):
    def fn():
        x, y = get_pos_x(), get_pos_y()
        if x == border[0] or y == border[1]:
            spawn_drone(diagonal_move_do(4, North, East, work_drone_task))
        work_drone_task()

    return fn


clear()
# debug purpose: move to center
# for _ in range(12):
#     move(North)
#     move(East)
center = (get_pos_x(), get_pos_y())
border = (center[0] + 12, center[1] + 12)
spawn_drone_task1()
