s = get_world_size()


def insertion_sort_vertical():
    while True:
        if get_pos_y() > 0:
            if measure() < measure(South):  # ty: ignore
                swap(South)
                move(South)
                continue
        break


def insertion_sort_horizontal():
    while True:
        if get_pos_x() > 0:
            if measure() < measure(West):  # ty: ignore
                swap(West)
                move(West)
                continue
        break

    if num_drones() == 1:
        harvest()

def move_to_x(tx):
    cx = get_pos_x()
    dx_east = (tx - cx) % s
    dx_west = s - dx_east
    if dx_east < dx_west:
        for _ in range(dx_east):
            move(East)
    else:
        for _ in range(dx_west):
            move(West)


def move_to_y(ty):
    cy = get_pos_y()
    dy_north = (ty - cy) % s
    dy_south = s - dy_north
    if dy_north < dy_south:
        for _ in range(dy_north):
            move(North)
    else:
        for _ in range(dy_south):
            move(South)


def straight_move_do(side_length, d, do):
    def fn():
        for _ in range(side_length):
            move(d)
        do()

    return fn


def horizontal_work():
    all_dispatched = False
    other_finished = False
    for y in range(s):
        all_dispatched = all_dispatched or num_drones() == s
        other_finished = other_finished or num_drones() < s
        move_to_y(y)
        till()
        plant(Entities.Cactus)
        if all_dispatched and other_finished:
            if spawn_drone(insertion_sort_vertical):
                continue
        insertion_sort_vertical()


def vertical_work():
    all_dispatched = False
    other_finished = False
    for x in range(s):
        all_dispatched = all_dispatched or num_drones() == s
        other_finished = other_finished or num_drones() < s
        move_to_x(x)
        if all_dispatched and other_finished:
            if spawn_drone(insertion_sort_horizontal):
                continue
        insertion_sort_horizontal()

    if num_drones() == 1:
        harvest()


for i in range(1, s // 2):
    spawn_drone(straight_move_do(i, East, horizontal_work))
for i in range(1, s // 2 + 1):
    spawn_drone(straight_move_do(i, West, horizontal_work))
horizontal_work()
while num_drones() != 1:
    pass

for i in range(1, s // 2):
    spawn_drone(straight_move_do(i, North, vertical_work))
for i in range(1, s // 2 + 1):
    spawn_drone(straight_move_do(i, South, vertical_work))
vertical_work()
