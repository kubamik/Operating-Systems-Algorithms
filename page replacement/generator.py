import random


def generate(npages, ncalls, min_group_size, max_group_size, min_group_length, max_group_length, **_):
    calls = []
    group = []
    group_length = 0
    group_chance = 1 / (max_group_length + min_group_length) * 3
    for _ in range(ncalls):
        if not group_length:
            if random.random() < group_chance:
                group_size = random.randint(min_group_size, max_group_size)
                group = random.sample(range(npages), group_size)
                group_length = random.randint(min_group_length, max_group_length)
            else:
                calls.append(random.randint(0, npages - 1))
                continue

        calls.append(random.choice(group))
        group_length -= 1

    return calls
