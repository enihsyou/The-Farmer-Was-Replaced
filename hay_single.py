# 周围三格种上草丛
for _ in range(3):
    move(North)
    plant(Entities.Bush)
move(North)
for _ in range(3):
    move(North)
    plant(Entities.Bush)

move(East)

for _ in range(3):
    plant(Entities.Bush)
    move(South)
move(South)
for _ in range(3):
    plant(Entities.Bush)
    move(South)

move(North)
move(North)
move(East)
for _ in range(5):
    plant(Entities.Bush)
    move(South)

move(East)
move(North)
for _ in range(3):
    move(North)
    plant(Entities.Bush)

move(East)
move(South)
plant(Entities.Bush)

move(East)
plant(Entities.Bush)

move(East)
move(North)
for _ in range(3):
    plant(Entities.Bush)
    move(South)

move(East)
for _ in range(5):
    plant(Entities.Bush)
    move(North)

move(East)
move(South)
move(South)
move(South)

while True:
    while get_water() < 0.8:
        use_item(Items.Water)
    harvest() # move 消耗的时间基本抵消了成长时间，无需 can_harvest()
    if num_items(Items.Hay) > 100000000:
        break
    c, (x, y) = get_companion()  # type: ignore
    while c != Entities.Bush or (x == 1 and y == 0):
        harvest()
        c, (x, y) = get_companion()  # type: ignore
    move(East)

    while get_water() < 0.8:
        use_item(Items.Water)
    harvest()
    if num_items(Items.Hay) > 100000000:
        break
    c, (x, y) = get_companion()  # type: ignore
    while c != Entities.Bush or (x == 0 and y == 0):
        harvest()
        c, (x, y) = get_companion()  # type: ignore
    move(West)
