def lru(i, call, frames, last_used):
    if call in frames:
        last_used[frames.index(call)] = i
        return False
    ret = None not in frames
    remove_page(i, call, frames, last_used)
    return ret


def remove_page(i, page, frames, last_used):
    idx = min(enumerate(last_used), key=lambda x: x[1])[0]
    if page != -1:
        frames[idx] = page
        last_used[idx] = i
    else:
        frames.pop(idx)
        last_used.pop(idx)
