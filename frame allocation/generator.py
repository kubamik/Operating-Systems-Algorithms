import random
from collections import deque


def generate(process_data, min_group_size, max_group_size, min_group_length, max_group_length, **__):
    pages = 0
    calls_split = []
    for npages, ncalls in process_data:
        calls_split.append(generate_for_process(pages, npages, ncalls, min_group_size, min(max_group_size, npages),
                                                min_group_length, max_group_length))
        pages += npages

    calls = []
    while len(calls_split) > 0:
        index = random.randint(0, len(calls_split) - 1)
        calls.append(calls_split[index].popleft())
        if len(calls_split[index]) == 0:
            calls_split.pop(index)

    return calls


def generate_for_process(
        start_page, npages, ncalls, min_group_size, max_group_size,
        min_group_length, max_group_length, factor=2, **_):
    calls = deque()
    group = []
    group_length = 0
    group_chance = 1 / (max_group_length + min_group_length) * 2 * factor
    for _ in range(ncalls):
        if not group_length:
            if random.random() < group_chance:
                group_size = random.randint(min_group_size, max_group_size)
                group = random.sample(range(start_page, start_page + npages), group_size)
                group_length = random.randint(min_group_length, max_group_length)
            else:
                calls.append(random.randint(start_page, start_page + npages - 1))
                continue

        calls.append(random.choice(group))
        group_length -= 1

    return calls
