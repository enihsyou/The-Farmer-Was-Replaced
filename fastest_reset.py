from __builtins__ import can_harvest, get_world_size, max_drones, num_drones

ITEM_TO_ENTITY = {
    Items.Hay: Entities.Grass,
    Items.Wood: Entities.Bush,
    Items.Carrot: Entities.Carrot,
    Items.Pumpkin: Entities.Pumpkin,
    Items.Cactus: Entities.Cactus,
    Items.Bone: Entities.Apple,
    Items.Weird_Substance: Entities.Tree,
    Items.Gold: Entities.Tree,
}


def get_unlock_cost(thing):
    # 计算总共需要每种物品多少个，包含种植成本
    unlock_cost = get_cost(thing, num_unlocked(thing)) or {}
    harvest_costs = []
    for item in unlock_cost:
        harvest_costs.append(get_harvest_cost(item, unlock_cost[item]))
    for item in harvest_costs:
        merge_dict(unlock_cost, item)
    return unlock_cost


def get_harvest_cost(item, amount):
    # 计算采收某个物品需要的种植成本
    s = get_world_size()
    buffer = s * s // 1.5
    item_have = num_items(item)
    item_need = max(amount - item_have + buffer, 0)
    item_cost = get_cost(ITEM_TO_ENTITY[item]) or {}
    harvest_cost = {}
    for seed in item_cost:
        plant_need = item_cost[seed] * item_need
        harvest_cost[seed] = plant_need
        merge_dict(harvest_cost, get_harvest_cost(seed, plant_need))
    return harvest_cost


def merge_dict(a, b):
    for key in b:
        if key not in a:
            a[key] = 0
        a[key] += b[key]
    return a


def pad_number(n):
    if n < 1:
        return "00"
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)


def format_time():
    t = get_time()
    h = t // 3600
    m = t % 3600 // 60
    s = t % 60 // 1
    ms = (t * 100) % 100 // 1
    return (
        pad_number(h) + ":" + pad_number(m) + ":" + pad_number(s) + "." + pad_number(ms)
    )


def unlock_timer(thing, unlock_cost):
    start_time = get_time()
    quick_print(format_time(), thing, num_unlocked(thing) + 1, "need", unlock_cost)

    def fn():
        time_cost = get_time() - start_time
        if unlock(thing):
            quick_print(format_time(), thing, "done in", time_cost, "seconds")
            return True
        else:
            quick_print(format_time(), "failed to unlock", thing)
            return False

    return fn


def unlock_tech(thing):
    unlock_cost = get_unlock_cost(thing)
    unlock_done = unlock_timer(thing, unlock_cost)

    # if num_unlocked(Unlocks.Sunflowers):
    #     harvest_sunflowers()
    if Items.Hay in unlock_cost:
        harvest_hay(unlock_cost[Items.Hay])
    if Items.Wood in unlock_cost:
        harvest_wood(unlock_cost[Items.Wood])
    if Items.Carrot in unlock_cost:
        harvest_carrots(unlock_cost[Items.Carrot])
    if Items.Pumpkin in unlock_cost:
        harvest_pumpkins(unlock_cost[Items.Pumpkin])
    if Items.Cactus in unlock_cost:
        harvest_cactus(unlock_cost[Items.Cactus])
    if Items.Bone in unlock_cost:
        harvest_bones(unlock_cost[Items.Bone])
    if Items.Weird_Substance in unlock_cost:
        harvest_weird_substance(unlock_cost[Items.Weird_Substance])
    if Items.Gold in unlock_cost:
        harvest_weird_substance(unlock_cost[Items.Gold])
        harvest_gold(unlock_cost[Items.Gold])

    if unlock_done():
        return
    unlock_tech(thing) # try again


def harvest_hay(amount):
    if num_unlocked(Unlocks.Megafarm):
        harvest_hay_multi_drone(amount)
    else:
        harvest_hay_single_drone(amount)


def harvest_hay_multi_drone(amount):
    s = get_world_size()

    def fn2():
        while num_items(Items.Hay) < amount:
            traverse_rectangle(polyfarm_hay(), s // 2, s)

    if max_drones() == 2:
        drone = spawn_drone(move_do((0, 0), fn2))
        move_do((s // 2, 0), fn2)()
        wait_for(drone)


def harvest_hay_single_drone(amount):
    traverse_fn = get_traverse_fn()

    def norm():
        if can_harvest():
            harvest()
        if get_entity_type() != Entities.Grass:
            harvest()
        if num_unlocked(Unlocks.Plant):
            plant(Entities.Grass)

    if num_unlocked(Unlocks.Polyculture):
        poly = polyfarm_hay()
        while num_items(Items.Hay) < amount:
            traverse_fn(poly)
    else:
        while num_items(Items.Hay) < amount:
            traverse_fn(norm)


def polyfarm_hay():
    wants = {}

    def poly():
        t = (get_pos_x(), get_pos_y())
        if t in wants:
            c = wants.pop(t)
            if get_entity_type() != c:
                harvest()
                if get_ground_type() != Grounds.Soil:
                    till()
                _ = plant(c) or plant(Entities.Grass)
            return
        while True:
            harvest()
            plant(Entities.Grass)
            c, pos = get_companion()
            if pos in wants and wants[pos] != c:
                continue
            wants[pos] = c
            break

    return poly


def harvest_wood(amount):
    if num_unlocked(Unlocks.Megafarm):
        harvest_wood_multi_drone(amount)
    else:
        harvest_wood_single_drone(amount)


def harvest_wood_multi_drone(amount):
    s = get_world_size()

    def fn2():
        while num_items(Items.Wood) < amount:
            traverse_rectangle(polyfarm_wood(), s // 2, s)

    if max_drones() == 2:
        drone = spawn_drone(move_do((0, 0), fn2))
        move_do((s // 2, 0), fn2)()
        wait_for(drone)


def harvest_wood_single_drone(amount):
    traverse_fn = get_traverse_fn()

    def use_bush():
        if can_harvest():
            harvest()
        if get_entity_type() != Entities.Bush:
            harvest()
        plant(Entities.Bush)

    def use_tree():
        if can_harvest():
            harvest()
        if get_pos_x() + get_pos_y() % 2:
            corp = Entities.Tree
        else:
            corp = Entities.Bush
        if get_entity_type() != corp:
            harvest()
        plant(corp)
        use_enough_water()

    if num_unlocked(Unlocks.Trees):
        if num_unlocked(Unlocks.Polyculture):
            poly = polyfarm_wood()
            while num_items(Items.Wood) < amount:
                traverse_fn(poly)
        else:
            while num_items(Items.Wood) < amount:
                traverse_fn(use_tree)
    else:
        while num_items(Items.Wood) < amount:
            traverse_fn(use_bush)


def polyfarm_wood():
    wants = {}

    def poly():
        t = (get_pos_x(), get_pos_y())
        if t in wants:
            c = wants.pop(t)
            if get_entity_type() != c:
                harvest()
                if get_ground_type() != Grounds.Soil:
                    till()
                _ = plant(c) or plant(Entities.Bush)
            return
        if not is_tree_pos(t):
            if can_harvest():
                harvest()
            plant(Entities.Bush)
            return
        while True:
            harvest()
            plant(Entities.Tree)
            c, pos = get_companion()
            if is_tree_pos(pos):
                continue
            if pos in wants and wants[pos] != c:
                continue
            wants[pos] = c
            break

    return poly


def harvest_carrots(amount):
    if num_unlocked(Unlocks.Megafarm):
        harvest_carrots_multi_drone(amount)
    else:
        harvest_carrots_single_drone(amount)


def harvest_carrots_multi_drone(amount):
    s = get_world_size()

    def fn2():
        while num_items(Items.Carrot) < amount:
            traverse_rectangle(polyfarm_carrots(), s // 2, s)

    if max_drones() == 2:
        drone = spawn_drone(move_do((0, 0), fn2))
        move_do((s // 2, 0), fn2)()
        wait_for(drone)


def harvest_carrots_single_drone(amount):
    traverse_fn = get_traverse_fn()

    def norm():
        if can_harvest():
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        if get_entity_type() != Entities.Carrot:
            harvest()
        plant(Entities.Carrot)

    if num_unlocked(Unlocks.Polyculture):
        poly = polyfarm_carrots()
        while num_items(Items.Carrot) < amount:
            traverse_fn(poly)
    else:
        while num_items(Items.Carrot) < amount:
            traverse_fn(norm)


def polyfarm_carrots():
    wants = {}

    def poly():
        t = (get_pos_x(), get_pos_y())
        if t in wants:
            c = wants.pop(t)
            if get_entity_type() != c:
                harvest()
                if get_ground_type() != Grounds.Soil:
                    till()
                _ = plant(c) or plant(Entities.Carrot)
            return
        while True:
            harvest()
            plant(Entities.Carrot)
            c, pos = get_companion()
            if pos in wants and wants[pos] != c:
                continue
            wants[pos] = c
            break

    return poly


def harvest_sunflowers():
    if num_unlocked(Unlocks.Megafarm):
        harvest_sunflowers_multi_drone()
    else:
        for _ in range(3):
            harvest_sunflowers_single_drone()


def harvest_sunflowers_multi_drone():
    pass


def harvest_sunflowers_single_drone():
    traverse_fn = get_traverse_fn()
    sunflower_dict = {}
    for petals in range(7, 16):
        sunflower_dict[petals] = []

    def fn():
        if can_harvest():
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Sunflower)
        sunflower_dict[measure()].append((get_pos_x(), get_pos_y()))

    traverse_fn(fn)
    sunflower_count = get_world_size() ** 2
    for petal in range(16, 6, -1):
        max_can_harvest = sunflower_count - 9
        tocheck, unripes = sunflower_dict[petal], []
        this_petal_harvest = min(max_can_harvest, len(tocheck))
        for _ in range(this_petal_harvest):
            while True:
                if not tocheck:
                    tocheck, unripes = unripes, []
                nearest = nearest_expect_current(tocheck)
                if nearest == None:
                    # 说明当前位置就是最后一个点
                    while not can_harvest():
                        use_item(Items.Fertilizer)
                    harvest()
                    break  # while loop
                else:
                    # 尝试采集，否则检查下一个
                    move_to(nearest)
                    if can_harvest() or use_item(Items.Fertilizer):
                        harvest()
                        tocheck.remove(nearest)
                        break  # while loop
                    else:
                        unripes.append(nearest)
        sunflower_count -= max(0, this_petal_harvest)


def nearest_expect_current(positions):
    # 找到离当前位置最近的点
    min_pos = None
    min_dis = 9999
    x, y = get_pos_x(), get_pos_y()
    for pos in positions:
        mx, my = pos
        dis = abs(mx - x) + abs(my - y)
        if dis == 0:
            continue
        if dis < min_dis:
            min_dis = dis
            min_pos = pos
    return min_pos


def harvest_cactus(amount):
    if num_unlocked(Unlocks.Megafarm):
        harvest_cactus_multi_drone(amount)
    else:
        for _ in range(3):
            harvest_cactus_single_drone(amount)


def harvest_cactus_multi_drone(amount):
    harvest_cactus_single_drone(amount)


def harvest_cactus_single_drone(amount):
    s = get_world_size()
    m = s - 1
    last_few = s * 2 - 3
    while num_items(Items.Cactus) < amount:
        move_to((0, 0))
        for i in range(s * 2):
            for j in range(i + 1):
                if j > m or i - j > m:
                    continue
                move_to((j, i - j))
                if get_ground_type() != Grounds.Soil:
                    till()
                if get_entity_type() != Entities.Cactus:
                    harvest()
                plant(Entities.Cactus)
                perform_insertion_sort()
                if i >= last_few:
                    force_growup()
        harvest()


def perform_insertion_sort():
    while True:
        v = measure()
        x, y = get_pos_x(), get_pos_y()
        vw = measure(West)
        vs = measure(South)
        if x != 0 and v < vw:  # type: ignore
            if y != 0 and vw < vs:  # type: ignore
                dir = South  # 和更大的一个交换，维持已有顺序
            else:
                dir = West
            swap(dir)
            move(dir)
            continue
        if y != 0 and v < vs:  # type: ignore
            if x != 0 and vs < vw:  # type: ignore
                dir = West
            else:
                dir = South
            swap(dir)
            move(dir)
            continue
        break


def harvest_pumpkins(amount):
    if num_unlocked(Unlocks.Megafarm):
        harvest_pumpkins_multi_drone(amount)
    else:
        harvest_pumpkins_single_drone(amount)


def harvest_pumpkins_multi_drone(amount):
    harvest_pumpkins_single_drone(amount)


def harvest_pumpkins_single_drone(amount):
    traverse_fn = get_traverse_fn()
    unripes = []

    def do_plant():
        if can_harvest():
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        if get_entity_type() != Entities.Pumpkin:
            harvest()
        plant(Entities.Pumpkin)

    def do_check():
        if plant(Entities.Pumpkin) or not can_harvest():
            unripes.append((get_pos_x(), get_pos_y()))
            use_enough_water()

    def force_check():
        if plant(Entities.Pumpkin) or not can_harvest():
            unripes.append((get_pos_x(), get_pos_y()))
            force_growup()

    while num_items(Items.Pumpkin) < amount:
        move_to((0, 0))
        traverse_fn(do_plant)
        traverse_fn(do_check)
        while unripes:
            move_to(unripes.pop(0))
            if num_items(Items.Carrot) < 1000:
                return
            force_check()
        harvest()
        unripes = []


def harvest_bones(amount):
    set_world_size(0)
    import dianosaus

    while num_items(Items.Bone) < amount:
        clear()
        dianosaus.harvest_dianosaus()


def harvest_weird_substance(amount):
    traverse_fn = get_traverse_fn()
    wants = {}
    while num_items(Items.Weird_Substance) < amount:

        def poly():
            t = (get_pos_x(), get_pos_y())
            if t in wants:
                c = wants.pop(t)
                if get_entity_type() != c:
                    if can_harvest():
                        use_item(Items.Weird_Substance)
                    harvest()
                    if get_ground_type() != Grounds.Soil:
                        till()
                    _ = plant(c) or plant(Entities.Grass)
                return
            while True:
                if can_harvest():
                    use_item(Items.Weird_Substance)
                harvest()
                plant(Entities.Grass)
                c, pos = get_companion()
                if pos in wants and wants[pos] != c:
                    continue
                wants[pos] = c
                break

        traverse_fn(poly)


def harvest_gold(amount):
    set_world_size(8)
    import maze_single

    while num_items(Items.Gold) < amount:
        clear()
        MULTIPLIER = 2 ** (num_unlocked(Unlocks.Mazes) - 1)
        # 迷宫大小
        MSIZE = 8
        # 需要的 Weird_Substance 数量
        maze_single.COSTS = MSIZE * MULTIPLIER
        # 能获得的 Gold 数量
        maze_single.COSTS = MSIZE * maze_single.COSTS
        maze_single.leaderboard()


def traverse_rectangle(fn, w, h):
    fn()
    move(North)
    for i in range(w, 0, -2):
        for j in range(h, 1, -1):
            fn()
            if j != 2:
                move(North)
        move(East)
        for j in range(h, 1, -1):
            fn()
            if j != 2:
                move(South)
        if i != 2:
            move(East)
    move(South)
    for _ in range(1, w):
        fn()
        move(West)


def traverse_wrap_border(fn):
    # 利用边界传送的特性，简单地遍历全图
    s = get_world_size()
    for _ in range(s):
        for _ in range(s):
            fn()
            move(North)
        move(East)


def traverse_loop_around(fn):
    # 哈密顿路径回到原点
    s = get_world_size()
    traverse_rectangle(fn, s, s)


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos
    s = get_world_size()

    dx_east = (tx - cx) % s
    dx_west = s - dx_east
    if dx_east < dx_west:
        for _ in range(dx_east):
            move(East)
    else:
        for _ in range(dx_west):
            move(West)

    dy_north = (ty - cy) % s
    dy_south = s - dy_north
    if dy_north < dy_south:
        for _ in range(dy_north):
            move(North)
    else:
        for _ in range(dy_south):
            move(South)


def get_traverse_fn():
    if get_world_size() % 2:
        return traverse_wrap_border
    else:
        return traverse_loop_around


def force_growup():
    while not can_harvest() and (use_item(Items.Fertilizer) or use_enough_water()):
        continue


def use_enough_water():
    w = get_water()
    if w < 0.75:
        n = min((1 - w) / 0.25 // 1, num_items(Items.Water))
        if n:
            use_item(Items.Water, n)


def is_tree_pos(p):
    x, y = p
    return (x + y) % 2 == 0


def move_do(pos, do):
    def fn():
        move_to(pos)
        do()

    return fn


unlock_tech(Unlocks.Speed)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Plant)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Speed)
unlock_tech(Unlocks.Carrots)
unlock_tech(Unlocks.Grass)
unlock_tech(Unlocks.Trees)
unlock_tech(Unlocks.Trees)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Carrots)
unlock_tech(Unlocks.Speed)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Watering)
unlock_tech(Unlocks.Watering)
unlock_tech(Unlocks.Carrots)
unlock_tech(Unlocks.Grass)
unlock_tech(Unlocks.Sunflowers)
unlock_tech(Unlocks.Fertilizer)
unlock_tech(Unlocks.Watering)
unlock_tech(Unlocks.Speed)
unlock_tech(Unlocks.Pumpkins)
unlock_tech(Unlocks.Watering)
unlock_tech(Unlocks.Polyculture)
unlock_tech(Unlocks.Speed)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Fertilizer)
unlock_tech(Unlocks.Mazes)
unlock_tech(Unlocks.Megafarm)
unlock_tech(Unlocks.Trees)
unlock_tech(Unlocks.Trees)
unlock_tech(Unlocks.Carrots)
unlock_tech(Unlocks.Watering)
unlock_tech(Unlocks.Pumpkins)
unlock_tech(Unlocks.Pumpkins)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Cactus)
unlock_tech(Unlocks.Hats)
unlock_tech(Unlocks.Dinosaurs)
unlock_tech(Unlocks.Dinosaurs)
unlock_tech(Unlocks.Pumpkins)
unlock_tech(Unlocks.Polyculture)
unlock_tech(Unlocks.Mazes)
unlock_tech(Unlocks.Mazes)
unlock_tech(Unlocks.Grass)
unlock_tech(Unlocks.Megafarm)
unlock_tech(Unlocks.Megafarm)
unlock_tech(Unlocks.Trees)
unlock_tech(Unlocks.Fertilizer)
unlock_tech(Unlocks.Fertilizer)
unlock_tech(Unlocks.Watering)
unlock_tech(Unlocks.Carrots)
unlock_tech(Unlocks.Carrots)
unlock_tech(Unlocks.Pumpkins)
unlock_tech(Unlocks.Expand)
unlock_tech(Unlocks.Megafarm)
unlock_tech(Unlocks.Cactus)
unlock_tech(Unlocks.Cactus)
unlock_tech(Unlocks.Dinosaurs)
unlock_tech(Unlocks.Dinosaurs)
unlock_tech(Unlocks.Dinosaurs)
unlock_tech(Unlocks.Mazes)
unlock_tech(Unlocks.Leaderboard)
quick_print(get_time(), "All done!")
