from util import Request, rt_request_entry


def scan(requests, size, queue=None, index=0,  position=0, movement=0, waiting_times=None, cycles=None, forward=True,
         *_, **__):
    if queue is None:
        queue = list()
    if waiting_times is None:
        waiting_times = list()
    if position == size-1:
        forward = False
    if position == 0 or forward is None:
        forward = True

    qindex = binary_search(queue, position, forward)

    while index != len(requests) or len(queue) > 0:
        position += (not forward) * (-2) + 1
        movement += 1
        added = False
        while index < len(requests) and requests[index].arrival <= movement:
            if isinstance(requests[index], rt_request_entry):
                break
            queue.append(Request(requests[index]))
            index += 1
            added = True
        if index < len(requests) and isinstance(requests[index], rt_request_entry):
            break

        if position == size-1 or position == 0:
            forward = not forward
            qindex = binary_search(queue, position, forward)
        if added:
            queue.sort()
            qindex = binary_search(queue, position, forward)

        while 0 <= qindex < len(queue) and queue[qindex].location == position:
            waiting_times.append(queue[qindex].waiting_time(movement))
            queue.pop(qindex)
            if not forward:
                qindex -= 1

    return queue, index, position, movement, waiting_times, cycles


def binary_search(array, value, forward=True):
    left = -1
    right = len(array)
    while left < right-1:
        mid = (left + right) // 2
        if array[mid].location < value or (array[mid].location == value and not forward):
            left = mid
        else:
            right = mid
    if forward:
        return right
    else:
        return left
