import random
from collections import defaultdict

from lru import lru


def proportional(nframes, process_data, calls, **__):
    frames, last_used = distribute(nframes, process_data)
    pages = []
    faults = defaultdict(set)
    calls_history = defaultdict(list)

    for i, (npages, _) in enumerate(process_data):
        pages.extend([i for _ in range(npages)])

    for i, call in enumerate(calls):
        pid = pages[call]
        calls_history[pid].append(i)
        fault = lru(i, call, frames[pid], last_used[pid])
        if fault:
            faults[pid].add(i)

    return faults, calls_history, 0


def distribute(nframes, process_data, dist_rest=True):
    sum_pages = sum([data[0] for data in process_data])
    if sum_pages == 0:
        nframes = 0
    frames = []
    last_used = []

    for data in process_data:
        frames.append([None for _ in range(data[0] * nframes // sum_pages)])
        last_used.append([-1 for _ in range(data[0] * nframes // sum_pages)])

    if dist_rest:
        rest = nframes - sum([len(f) for f in frames])
        while rest > 0:
            idx = random.choice([i for i, data in enumerate(process_data) if data[0] > 0])
            frames[idx].append(None)
            last_used[idx].append(-1)
            rest -= 1

    return frames, last_used
