s = get_world_size()
m = s - 1


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


def work_plant():
    petal_count = [[], [], [], [], [], [], [], [], []]
    for _ in range(s):
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Sunflower)
        petal_count[measure() - 7].append(get_pos_y())
        if measure() >= 14:
            w = min(
                4 - 4 * get_water() // 1,
                get_pos_y() // 8,
                num_items(Items.Water),
            )
            if w:
                use_item(Items.Water, w)
        move(North)
    return petal_count


def work_harvest_petal(field_x_array):
    def fn():
        line = field_x_array[get_pos_x()]

        for p in range(15 - 7, -1, -1):
            for y in line[p]:
                move_to_y(y)
                if measure() == None:
                    continue
                while not can_harvest():
                    if use_item(Items.Fertilizer):
                        continue
                    w = min(
                        4 - 4 * get_water() // 1,
                        num_items(Items.Water),
                    )
                    if w:
                        use_item(Items.Water, w)
                harvest()
            if p == 0:
                # 最后一轮了，不用通知其他人
                return

            if not line[p]:
                # 本列没有这个花瓣数的向日葵了，随便清理一株以种草
                harvest()

            # 种草通知本列完成
            hay = num_items(Items.Hay)
            div = hay // (512 * 32)
            mod = hay % (512 * 32)
            plant(Entities.Grass)
            while not can_harvest():
                if get_water() < 0.75:
                    num_items(Items.Water)
            harvest()
            # 提前移动到下一个位置
            if p and line[p - 1]:
                move_to_y(line[p - 1][0])
            # 集齐 32 列说明本轮完成了
            while True:
                if num_items(Items.Power) > 100000:
                    return
                hay_now = num_items(Items.Hay)
                div_now = hay_now // (512 * 32)
                mod_now = hay_now % (512 * 32)
                if div_now != div or mod_now < mod or mod_now == 0:
                    break


    return fn


def sender(dir, main, work):
    def fn():
        if main:
            move(dir)
        drones = {}
        for _ in range(1, s // 2):
            drones[get_pos_x()] = spawn_drone(work)
            move(dir)
        self_result = work()
        for x in drones:
            drones[x] = wait_for(drones[x])
        drones[get_pos_x()] = self_result
        return drones

    return fn


while num_items(Items.Power) < 100000:
    field_x_array = {}
    worker1 = sender(West, False, work_plant)
    worker2 = sender(East, True, work_plant)
    forked = spawn_drone(worker1)
    worker2_return = worker2()
    worker1_return = wait_for(forked)
    for x in worker1_return:
        field_x_array[x] = worker1_return[x]
    for x in worker2_return:
        field_x_array[x] = worker2_return[x]

    work = work_harvest_petal(field_x_array)
    worker1 = sender(West, False, work)
    worker2 = sender(East, True, work)
    forked = spawn_drone(worker1)
    worker2_return = worker2()
    worker1_return = wait_for(forked)
