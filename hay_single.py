from __builtins__ import can_harvest, harvest, North, East, West, South, get_companion, Entities

s = get_world_size()
m = s - 1
bush_companions = set()

for _ in range(m):
    plant(Entities.Bush)
    move(North)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 0):
    plant(Entities.Bush)
    move(East)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 0):
    plant(Entities.Bush)
    move(South)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 1):
    plant(Entities.Bush)
    move(West)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 1):
    plant(Entities.Bush)
    move(North)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 2):
    plant(Entities.Bush)
    move(East)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 2):
    plant(Entities.Bush)
    move(South)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 3):
    plant(Entities.Bush)
    move(West)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 3):
    plant(Entities.Bush)
    move(North)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 4):
    plant(Entities.Bush)
    move(East)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 4):
    plant(Entities.Bush)
    move(South)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 5):
    plant(Entities.Bush)
    move(West)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 5):
    plant(Entities.Bush)
    move(North)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

for _ in range(m - 6):
    plant(Entities.Bush)
    move(East)
    bush_companions.add((Entities.Bush, (get_pos_x(), get_pos_y())))

while num_items(Items.Hay) < 100000000:
    if can_harvest():
        harvest()
        while get_companion() not in bush_companions:
            harvest()
        if get_water() < 0.85:
            use_item(Items.Water)
    move(South)

    if can_harvest():
        harvest()
        while get_companion() not in bush_companions:
            harvest()
        if get_water() < 0.85:
            use_item(Items.Water)
    move(North)
