from collections import defaultdict

from lru import lru, remove_page
from proportional import distribute


def working_sets(nframes, process_data, calls, c, wst, **__):
    original_process_data = process_data.copy()
    t = wst
    frames, last_used = distribute(nframes, process_data)
    pages = []
    faults = defaultdict(set)
    paused = set()
    pauses = 0
    pause_frames = {}
    last_calls = []
    calls_history = defaultdict(list)
    calls_left = [data[1] for data in process_data]

    for i, (npages, _) in enumerate(process_data):
        pages.extend([i for _ in range(npages)])

    for i, call in enumerate(calls):
        pid = pages[call]
        if pid in paused:
            calls.append(call)
            continue

        fault = lru(i, call, frames[pid], last_used[pid])
        last_calls.append(call)
        if fault:
            faults[pid].add(i)
        calls_history[pid].append(i)

        calls_left[pid] -= 1
        if calls_left[pid] == 0:
            free = len(frames[pid])
            process_data[pid] = (0, 0)
            frames[pid] = []
            last_used[pid] = []
            if len(paused):
                pid = min(paused)
                paused.remove(pid)
                process_data[pid] = original_process_data[pid]
                frame_count = min(free, pause_frames[pid])
                frames[pid] = [None for _ in range(frame_count)]
                last_used[pid] = [-1 for _ in range(frame_count)]
                free -= frame_count
            if sum(calls_left) > 0:
                distribute_append(free, frames, last_used, process_data)

        if len(last_calls) >= t:
            if i % c == 0:
                ws = [set() for _ in process_data]
                for cl in last_calls:
                    pid = pages[cl]
                    if process_data[pid][0] != 0:
                        ws[pid].add(cl)

                for pid, w in enumerate(ws):
                    if process_data[pid][0] != 0 and len(w) == 0:
                        w.add(-1)

                d = sum(len(w) for w in ws)
                while d > nframes:
                    pid = ws.index(max(ws, key=lambda data: len(data)))
                    paused.add(pid)
                    process_data[pid] = (0, 0)
                    pause_frames[pid] = len(frames[pid])
                    frames[pid] = []
                    last_used[pid] = []
                    d -= len(ws[pid])
                    pauses += 1
                    ws[pid] = []

                for pid, data in enumerate(ws):
                    if process_data[pid][0] == 0:
                        continue
                    while len(frames[pid]) < max(1, len(data)):
                        frames[pid].append(None)
                        last_used[pid].append(-1)
                    while len(frames[pid]) > max(1, len(data)):
                        remove_page(0, -1, frames[pid], last_used[pid])
                if nframes > d > 0:
                    distribute_append(nframes - d, frames, last_used, process_data)
                pass

            last_calls.pop(0)

    return faults, calls_history, pauses


def distribute_append(nframes, frames, last_used, process_data):
    new_frames, new_last_used = distribute(nframes, process_data)
    for data, new_data in zip(frames, new_frames):
        data.extend(new_data)
    for data, new_data in zip(last_used, new_last_used):
        data.extend(new_data)
