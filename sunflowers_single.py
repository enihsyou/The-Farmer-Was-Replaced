# set_world_size(8)
s = get_world_size()
m = s - 1


def traverse_topdown_no_if(fn):
    for i in range(0, s, 2):
        for j in range(m):
            fn(i)
            move(North)
        fn(i)
        move(East)
        for j in range(m):
            fn(i)
            move(South)
        fn(i)
        move(East)


def move_to(pos):
    cx, cy = get_pos_x(), get_pos_y()
    tx, ty = pos

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


W = 0.75


def plant_a_sunflower_first(i):
    till()
    plant(Entities.Sunflower)
    sunflower_dict[measure()].append((get_pos_x(), get_pos_y()))
    if i < s - 2:
        # 只给最后两列浇水，因为前面的已经长好了
        return
    while get_water() < W:
        use_item(Items.Water)


def plant_a_sunflower(_):
    # plant 会在已有植物上 return False
    if plant(Entities.Sunflower):
        v = measure()
        sunflower_dict[v].append((get_pos_x(), get_pos_y()))
        if v <= 10:  # ty: ignore
            # 采集其他的时间足够它生长了
            return
        while get_water() < W:
            use_item(Items.Water)


sunflower_dict = {}  # 记录不同花瓣数的向日葵位置
for petals in range(7, 16):
    sunflower_dict[petals] = []

MAX_PETALS = 15
MIN_PETALS = 7
MIN_PETALS_S1 = 6  # MIN_PETALS -1
FULL_GROUND = s * s  # 田块总数
OCTUPLE_BASE = 10
OCTUPLE_BASE_S1 = 9  # OCTUPLE_BASE - 1


# 平均每轮收集至少 430 能量
def trip_round():
    sunflower_count = FULL_GROUND  # 肯定种满了，直接赋值
    for petal in range(MAX_PETALS, MIN_PETALS_S1, -1):
        # 为了维持场上至少 10 株，最多采集这么多
        max_can_harvest = sunflower_count - OCTUPLE_BASE_S1
        tocheck, unripes = sunflower_dict[petal], []
        this_petal_harvest = min(max_can_harvest, len(tocheck))
        for _ in range(this_petal_harvest):
            while True:
                if tocheck:
                    pos = tocheck.pop()
                    move_to(pos)
                    if can_harvest():
                        harvest()
                        break  # while loop
                    else:
                        unripes.append(pos)
                else:
                    tocheck, unripes = unripes, []
        sunflower_count -= max(0, this_petal_harvest)
    # 场面上应该剩余 9 株向日葵，开始种植新的
    traverse_topdown_no_if(plant_a_sunflower)


# 最后几轮收集添加数量判断提前结束
def last_trip_round():
    sunflower_count = FULL_GROUND
    for petal in range(MAX_PETALS, MIN_PETALS_S1, -1):
        max_can_harvest = sunflower_count - OCTUPLE_BASE_S1
        tocheck, unripes = sunflower_dict[petal], []
        this_petal_harvest = min(max_can_harvest, len(tocheck))
        for _ in range(this_petal_harvest):
            while True:
                if tocheck:
                    pos = tocheck.pop()
                    move_to(pos)
                    if can_harvest():
                        harvest()
                        break  # while loop
                    else:
                        unripes.append(pos)
                else:
                    tocheck, unripes = unripes, []
            if num_items(Items.Power) > 10000:
                return
        sunflower_count -= max(0, this_petal_harvest)
    traverse_topdown_no_if(plant_a_sunflower)


traverse_topdown_no_if(plant_a_sunflower_first)
for _ in range(22):
    trip_round()
while num_items(Items.Power) < 10000:
    last_trip_round()
