def opt(npages, nframes, calls):
    frames = [None] * nframes
    faults = 0
    for i, call in enumerate(calls):
        if call in frames:
            continue

        faults += 1
        if None in frames:
            frames[frames.index(None)] = call
            continue

        pages = {p for p in range(npages) if p in frames}
        for page in calls[i+1:]:
            if page in pages:
                pages.remove(page)
            if len(pages) == 1:
                break

        page = pages.pop()
        frames[frames.index(page)] = call

    return faults
