s = get_world_size()


def cocktail_forward(start, end, direction):
    swapped = False
    for i in range(start, end):
        if measure() > measure(direction):  # ty: ignore
            swap(direction)
            swapped = True
        if i != end - 1:
            move(direction)
    return swapped


def cocktail_backward(start, end, direction):
    swapped = False
    for i in range(end - 1, start - 1, -1):
        if measure() < measure(direction):  # ty: ignore
            swap(direction)
            swapped = True
        if i != start:
            move(direction)
    return swapped


def straight_move_do(side_length, d, do):
    def fn():
        for _ in range(side_length):
            move(d)
        do()

    return fn


def horizontal_work():
    forked = spawn_drone(straight_move_do(1, East, horizontal_work))
    for _ in range(s):
        till()
        plant(Entities.Cactus)
        if get_pos_y() > 0 and measure() < measure(South):  # ty: ignore
            swap(South)
        move(North)

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

    if forked:
        wait_for(forked)


def vertical_work():
    forked = spawn_drone(straight_move_do(1, North, vertical_work))
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

    if forked:
        wait_for(forked)


horizontal_work()
vertical_work()
harvest()
