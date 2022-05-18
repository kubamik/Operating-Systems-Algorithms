from collections import deque


def approx_lru(_, nframes, calls):
    frames = [None] * nframes
    faults = 0
    queue = deque([(False, None) for _ in range(nframes)])
    for call in calls:
        if call in frames:
            if (False, call) in queue:
                queue[queue.index((False, call))] = (True, call)
            continue

        while queue[0][0]:
            _, page = queue.popleft()
            queue.append((False, page))

        _, page = queue.popleft()
        frames[frames.index(page)] = call
        queue.append((True, call))
        faults += 1

    return faults
