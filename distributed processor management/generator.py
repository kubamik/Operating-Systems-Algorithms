import random

from utils import process_entry


def generate(n, gen):
    strategies = random.choices(gen, [g[-1] for g in gen], k=n)
    processes = []
    for min_l, max_l, min_w, max_w, min_d, max_d, min_c, max_c, _ in strategies:
        processes.append(list())
        c = random.randint(min_c, max_c)
        time = 0
        for _ in range(c):
            time += random.randint(min_d, max_d)
            processes[-1].append(process_entry(random.randint(min_w, max_w), time, random.randint(min_l, max_l)))

    return processes
