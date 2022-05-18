from random import randint


def rand(_, nframes, calls):
    frames = [None] * nframes
    faults = 0
    for call in calls:
        if call in frames:
            continue
        if None in frames:
            frames[frames.index(None)] = call
        else:
            frames[randint(0, nframes - 1)] = call
        faults += 1

    return faults
