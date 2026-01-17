# 周围三格种上草丛
from __builtins__ import Entities, get_companion

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

while num_items(Items.Hay) < 100000000:
    while not can_harvest():
        continue
    harvest()
    c, (x, y) = get_companion()  # type: ignore
    while c != Entities.Bush or (x == 1 and y == 0):
        harvest()
        c, (x, y) = get_companion()  # type: ignore
    while get_water() < 0.85:
        use_item(Items.Water)
    move(East)

    while not can_harvest():
        continue
    harvest()
    c, (x, y) = get_companion()  # type: ignore
    while c != Entities.Bush or (x == 0 and y == 0):
        harvest()
        c, (x, y) = get_companion()  # type: ignore
    while get_water() < 0.85:
        use_item(Items.Water)
    move(West)
