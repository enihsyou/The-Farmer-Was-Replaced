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
    while get_water() < W:
        use_item(Items.Water)
    while not can_harvest():
        if use_item(Items.Fertilizer):
            use_item(Items.Weird_Substance)
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


def spawn_drone_task2():
    for _ in range(3):
        spawn_drone(work_drone_task)
        for _ in range(8):
            move(East)
    work_drone_task()


def spawn_drone_task1():
    for _ in range(7):
        spawn_drone(spawn_drone_task2)
        for _ in range(4):
            move(East)
        for _ in range(4):
            move(North)
    spawn_drone_task2()


clear()
spawn_drone_task1()
