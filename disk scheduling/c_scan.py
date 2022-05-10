from util import Request, rt_request_entry


def c_scan(requests, size, queue=None, index=0,  position=0, movement=0, waiting_times=None, cycles=None, *_, **__):
    if queue is None:
        queue = list()
    if waiting_times is None:
        waiting_times = list()
    if cycles is None:
        cycles = 0

    qindex = binary_search(queue, position)

    data = []

    while index != len(requests) or len(queue) > 0:
        position += 1
        movement += 1

        if position == size:
            position = 0
            qindex = 0
            cycles += 1

        added = False
        while index < len(requests) and requests[index].arrival <= movement:
            if isinstance(requests[index], rt_request_entry):
                break
            queue.append(Request(requests[index]))
            index += 1
            added = True
        if index < len(requests) and isinstance(requests[index], rt_request_entry):
            break



        if added:
            queue.sort()
            qindex = binary_search(queue, position)

        while 0 <= qindex < len(queue) and queue[qindex].location == position:
            waiting_times.append(queue[qindex].waiting_time(movement))
            data.append(queue.pop(qindex).location)

    return queue, index, position, movement, waiting_times, cycles


def binary_search(array, value):
    left = -1
    right = len(array)
    while left < right-1:
        mid = (left + right) // 2
        if array[mid].location < value:
            left = mid
        else:
            right = mid
    return right
