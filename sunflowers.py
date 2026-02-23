from __builtins__ import get_ground_type, harvest

s = get_world_size()
m = s - 1


def work_plant():
    for _ in range(s):
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Sunflower)
        move(North)
        if measure() == 15:
            use_item(Items.Water, min(max(1, get_pos_y() // 8), num_items(Items.Water)))


def work_harvest_petal(size):
    def fn():
        for _ in range(s):
            if measure() == size:
                while not can_harvest():
                    if use_item(Items.Fertilizer):
                        continue
                    n = ((1 - get_water()) / 0.25) // 1
                    if n and n <= num_items(Items.Water):
                        use_item(Items.Water, n)
                harvest()
            move(North)

    return fn


def sender(dir, main, work):
    def fn():
        if main:
            move(dir)
        drones = []
        for _ in range(1, s // 2):
            drones.append(spawn_drone(work))
            move(dir)
        work()
        for drone in drones:
            wait_for(drone)

    return fn


while num_items(Items.Power) < 100000:
    worker1 = sender(West, False, work_plant)
    worker2 = sender(East, True, work_plant)
    forked = spawn_drone(worker1)
    worker2()
    wait_for(forked)

    for i in range(15, 6, -1):
        work = work_harvest_petal(i)
        worker1 = sender(West, False, work)
        worker2 = sender(East, True, work)
        forked = spawn_drone(worker1)
        worker2()
        wait_for(forked)
