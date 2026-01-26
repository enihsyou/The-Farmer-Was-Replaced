# 测试经验
# - for range 比 while count 更快
# - if chain 和 a and b 速度相同
# - string 做键时长度应控制在 16 以下
# - 超过 2 个元素的 tuple 可以尝试转成 string 再做键
# - tuple unpack 比 index 更快
# - while 循环用 continue 比 pass 做循环体更快
# - 等待成长用 while not can_harvest(): continue
# - list.pop() 比 list.pop(0) 更快
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
    a = [1,2,3,4,5]
    a.pop()

for _ in range(100):
    print_ticks(bench_target)
