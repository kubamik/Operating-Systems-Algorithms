def fifo(_, nframes, calls):
    frames = [None] * nframes
    last_removed = nframes - 1
    faults = 0
    for call in calls:
        if call in frames:
            continue
        last_removed = (last_removed + 1) % nframes
        frames[last_removed] = call
        faults += 1

    return faults
