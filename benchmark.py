# 测试经验
# - for range 比 while count 更快
# - if chain 和 a and b 速度相同
# - string 做键时长度应控制在 16 以下
# - 超过 2 个元素的 tuple 可以尝试转成 string 再做键
# - tuple unpack 比 index 更快
# - while 循环用 continue 比 pass 做循环体更快
# - 等待成长用 while not can_harvest(): continue
# - list.pop() 比 list.pop(0) 更快, 建议使用双栈模拟队列
from __builtins__ import quick_print, use_item


def print_ticks(fn):
    start_time = get_time()
    start_tick = get_tick_count()
    fn()
    end_tick = get_tick_count()
    end_time = get_time()
    # 减去调用 fn 消耗的 1 tick
    quick_print(
        "[benchmark]:",
        end_tick - start_tick - 1,
        "ticks",
        end_time - start_time,
        "seconds",
    )


def do_pop():
    a = []
    for i in range(100):
        a.append(i)
    for i in range(50):
        a.pop()
    for i in range(50):
        a.append(i)
    for i in range(100):
        a.pop()


def do_pop0():
    a = []
    for i in range(100):
        a.append(i)
    for i in range(50):
        a.pop(0)
    for i in range(50):
        a.append(i)
    for i in range(100):
        a.pop(0)


def sim_queue():
    ins, out = [], []

    def enqueue(x):
        ins.append(x)

    def dequeue():
        if not out:
            while ins:
                out.append(ins.pop())
        return out.pop()

    for i in range(100):
        enqueue(i)
    for i in range(50):
        enqueue(i)
    for i in range(50):
        dequeue()
    for i in range(100):
        dequeue()


def bench_target():
    do_pop()


print_ticks(do_pop)
print_ticks(do_pop0)
print_ticks(sim_queue)
