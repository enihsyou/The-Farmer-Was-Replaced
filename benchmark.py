# 测试经验
# - for range 比 while count 更快
# - if chain 和 a and b 速度相同
# - string 做键时长度应控制在 16 以下
# - 超过 2 个元素的 tuple 可以尝试转成 string 再做键
# - tuple unpack 比 index 更快
# - while 循环用 continue 比 pass 做循环体更快
# - 等待成长用 while not can_harvest(): continue
from __builtins__ import (
    East,
    Entities,
    Hats,
    South,
    can_harvest,
    change_hat,
    get_companion,
    harvest,
    quick_print,
    set_world_size,
)
from library import *


def print_ticks(fn):
    start_tick = get_tick_count()
    fn()
    end_tick = get_tick_count()
    # 减去调用 fn 消耗的 1 tick
    print("[benchmark]:", end_tick - start_tick - 1, "ticks")


def way1():
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

def way2():
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

    move(South)
    move(East)

    for _ in range(2):
        plant(Entities.Bush)
        move(South)
    move(South)
    move(South)
    for _ in range(3):
        move(South)
        plant(Entities.Bush)

    move(East)
    plant(Entities.Bush)
    move(North)
    plant(Entities.Bush)
    move(South)
    move(South)
    plant(Entities.Bush)
    move(North)

    move(East)
    plant(Entities.Bush)


    move(East)
    plant(Entities.Bush)


    move(East)
    plant(Entities.Bush)
    move(North)
    plant(Entities.Bush)
    move(South)
    move(South)
    plant(Entities.Bush)
    move(North)

    move(East)
    move(South)
    for _ in range(2):
        plant(Entities.Bush)
        move(South)
    move(South)
    move(South)
    for _ in range(3):
        move(South)
        plant(Entities.Bush)

    move(East)



def bench_target():
    way1()

set_world_size(8)
print_ticks(bench_target)

while True:
    pass
