# 测试经验
# - for range 比 while count 更快
# - if chain 和 a and b 速度相同
# - string 做键时长度应控制在 16 以下
# - 超过 2 个元素的 tuple 可以尝试转成 string 再做键
# - tuple unpack 比 index 更快
# - while 循环用 continue 比 pass 做循环体更快
# - 等待成长用 while not can_harvest(): continue
from __builtins__ import use_item, quick_print


def print_ticks(fn):
    start_time = get_time()
    start_tick = get_tick_count()
    fn()
    end_tick = get_tick_count()
    end_time = get_time()
    # 减去调用 fn 消耗的 1 tick
    quick_print("[benchmark]:", end_tick - start_tick - 1, "ticks", end_time - start_time, "seconds")


def bench_target():
    while not can_harvest():
        continue
    harvest()
    c, _ = get_companion()  # type: ignore
    while c != Entities.Bush:
        harvest()
        c, _ = get_companion()  # type: ignore
    while get_water() < 0.85:
        use_item(Items.Water)


set_world_size(3)
for _ in range(100):
    print_ticks(bench_target)
