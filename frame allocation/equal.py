import random
from collections import defaultdict

from lru import lru


def equal(nframes, process_data, calls, **__):
    frames_per_process = nframes // len(process_data)
    frames = []
    last_used = []
    pages = []
    faults = defaultdict(set)
    calls_history = defaultdict(list)

    for _ in range(len(process_data)):
        frames.append([None for i in range(frames_per_process)])
        last_used.append([-1 for i in range(frames_per_process)])
    for i, (npages, _) in enumerate(process_data):
        pages.extend([i for _ in range(npages)])

    rest = nframes - frames_per_process * len(process_data)
    while rest > 0:
        idx = random.randint(0, len(process_data) - 1)
        frames[idx].append(None)
        last_used[idx].append(-1)
        rest -= 1

    for i, call in enumerate(calls):
        pid = pages[call]
        calls_history[pid].append(i)
        fault = lru(i, call, frames[pid], last_used[pid])
        if fault:
            faults[pid].add(i)

    return faults, calls_history, 0

