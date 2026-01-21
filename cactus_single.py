from __builtins__ import set_world_size
set_world_size(8)
s = 8
m = s - 1


def traverse_topdown(fn):
    # 宽度为 2 的逆时针圈不断向东
    for i in range(0, s, 2):
        for j in range(s - 1):
            fn()
            move(North)
        fn()
        move(East)
        for j in range(s - 1):
            fn()
            move(South)
        fn()
        move(East)
    return False


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

    dx_east = (tx - cx) % s
    dx_west = (cx - tx) % s
    if dx_east < dx_west:
        for _ in range(dx_east):
            move(East)
    else:
        for _ in range(dx_west):
            move(West)

    dy_north = (ty - cy) % s
    dy_south = (cy - ty) % s
    if dy_north < dy_south:
        for _ in range(dy_north):
            move(North)
    else:
        for _ in range(dy_south):
            move(South)


def cocktail_forward(start, end, direction):
    swapped = False
    for i in range(start, end):
        if measure() > measure(direction):  # type: ignore
            swap(direction)
            swapped = True
        if i != end - 1:
            move(direction)
    return swapped


def cocktail_backward(start, end, direction):
    swapped = False
    for i in range(end - 1, start - 1, -1):
        if measure() < measure(direction):  # type: ignore
            swap(direction)
            swapped = True
        if i != start:
            move(direction)
    return swapped


def plant_a_cactus():
    till()
    plant(Entities.Cactus)


traverse_topdown(plant_a_cactus)

x = get_pos_x()
for i in range(s):
    move_to(((x + i) % s, 0))
    l, r = 0, s - 1
    while True:
        swapped = cocktail_forward(l, r, North)
        if not swapped:
            break
        r -= 1
        swapped = cocktail_backward(l, r, South)
        if not swapped:
            break
        l += 1
y = get_pos_y()
for i in range(s):
    move_to((0, (y + i) % s))
    l, r = 0, s - 1
    while True:
        swapped = cocktail_forward(l, r, East)
        if not swapped:
            break
        r -= 1
        swapped = cocktail_backward(l, r, West)
        if not swapped:
            break
        l += 1

harvest()
