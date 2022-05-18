def lru(_, nframes, calls):
    frames = [None] * nframes
    faults = 0
    last_used = [-1 for _ in range(nframes)]
    for i, call in enumerate(calls):
        if call in frames:
            last_used[frames.index(call)] = i
            continue

        idx = min(enumerate(last_used), key=lambda x: x[1])[0]
        frames[idx] = call
        last_used[idx] = i
        faults += 1

    return faults
