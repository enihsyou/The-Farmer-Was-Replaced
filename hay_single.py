s = get_world_size()
m = s - 1

dirs = [North, East, South, West]

# 总共需要走的段数是 2m + 1
# 例如 m=1时，走 N, E, S (3段)
for i in range(2 * m + 1):
    # 核心魔法：构造步长序列 m, m, m, m-1, m-1...
    # 当 i=0,1,2 时，reduction 为 0；当 i=3,4 时，为 1...
    reduction = max(0, i - 1) // 2
    current_len = m - reduction

    # 获取当前方向
    current_dir = dirs[i % 4]

    for _ in range(current_len):
        plant(Entities.Bush)
        move(current_dir)

while num_items(Items.Hay) < 100000000:
    while True:
        companion, _ = get_companion()  # type: ignore
        if companion == Entities.Bush:
            break
        harvest()
    while not can_harvest():
        continue
    while get_water() < 0.90:
        use_item(Items.Water)
    harvest()
