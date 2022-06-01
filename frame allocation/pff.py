from collections import defaultdict

from proportional import distribute
from lru import lru, remove_page


def pff(nframes, process_data, calls, u, l, pfft, **__):
    original_process_data = process_data.copy()
    t = pfft
    frames, last_used = distribute(nframes, process_data)
    pages = []
    faults = defaultdict(set)
    paused = set()
    pauses = 0
    pause_frames = {}
    last_calls = defaultdict(set)
    calls_history = defaultdict(list)
    free = 0
    calls_left = [data[1] for data in process_data]
    last_pff = defaultdict(float)

    for i, (npages, _) in enumerate(process_data):
        pages.extend([i for _ in range(npages)])

    for i, call in enumerate(calls):
        pid = pages[call]
        if pid in paused:
            calls.append(call)
            continue

        fault = lru(i, call, frames[pid], last_used[pid])
        last_calls[pid].add(i)
        if fault:
            faults[pid].add(i)
        calls_history[pid].append(i)

        calls_left[pid] -= 1
        if calls_left[pid] == 0:
            process_data[pid] = (0, 0)
            if len(paused):
                free += len(frames[pid])
                new_pid = min(paused)
                paused.remove(new_pid)
                process_data[new_pid] = original_process_data[new_pid]
                frame_count = min(free, pause_frames[new_pid] + 1)
                frames[new_pid] = [None for _ in range(frame_count)]
                last_used[new_pid] = [-1 for _ in range(frame_count)]
                free -= frame_count
            elif sum(calls_left) > 0:
                distribute_append(len(frames[pid]), frames, last_used, process_data)
            frames[pid] = []
            last_used[pid] = []
            continue

        if len(last_calls[pid]) >= t:
            f = len(last_calls[pid] & faults[pid])
            # f = len(set(range(i-t+1, i+1)) & faults[pid])
            pffi = f / len(last_calls[pid])
            if pffi >= u and pffi > last_pff[pid]:
                last_pff[pid] = pffi
                if free:
                    free -= 1
                    frames[pid].append(None)
                    last_used[pid].append(-1)
                elif len(frames[pid]) < nframes and frames[pid].count(None) == 0:
                    pauses += 1
                    paused.add(pid)
                    pause_frames[pid] = len(frames[pid])
                    process_data[pid] = (0, 0)
                    distribute_append(len(frames[pid]), frames, last_used, process_data)
                    frames[pid] = []
                    last_used[pid] = []
            elif pffi < l:
                last_pff[pid] = pffi
            if pffi <= l and len(frames[pid]) > 1:
                free += 1
                remove_page(0, -1, frames[pid], last_used[pid])
            last_calls[pid].remove(min(last_calls[pid]))

    return faults, calls_history, pauses


def distribute_append(nframes, frames, last_used, process_data):
    new_frames, new_last_used = distribute(nframes, process_data)
    for data, new_data in zip(frames, new_frames):
        data.extend(new_data)
    for data, new_data in zip(last_used, new_last_used):
        data.extend(new_data)