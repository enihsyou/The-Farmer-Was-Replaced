# 测试经验
# - for range 比 while count 更快
# - if chain 和 a and b 速度相同
# - string 做键时长度应控制在 16 以下
# - 超过 2 个元素的 tuple 可以尝试转成 string 再做键
# - tuple unpack 比 index 更快
from library import *


def print_ticks(fn):
    start_tick = get_tick_count()
    fn()
    end_tick = get_tick_count()
    # 减去调用 fn 消耗的 1 tick
    print("[benchmark]:", end_tick - start_tick - 1, "ticks")


def idle():
    pass


def bench_target():
    move_2d_torus(zeroing_position)
    change_hat(Hats.Dinosaur_Hat)
    move_2d_flat((0, 11))
    move_2d_flat((11, 11))



clear()
print_ticks(bench_target)
