from util import Request, RealTimeRequest, rt_request_entry


def fd_scan(requests, size, queue, index, position, movement, waiting_times, *__, unrealized_count=0,
            real_time_data=None):
    if real_time_data is None:
        real_time_data = []

    rt_queue = [RealTimeRequest(requests[index])]
    index += 1
    req = rt_queue[0]
    if not req.can_do(movement, position):
        return queue, index, position, movement, waiting_times, None, unrealized_count+1, real_time_data
    forward = None if req.location == position else req.location > position
    sorted_queue = sorted(queue)
    qindex = binary_search(sorted_queue, position, forward or forward is None)
    rtqindex = binary_search(rt_queue, position, forward or forward is None)

    while len(rt_queue) > 0:
        if forward is not None:
            position += (not forward) * (-2) + 1
            movement += 1
        added = False
        while index < len(requests) and requests[index].arrival <= movement:
            if isinstance(requests[index], rt_request_entry):
                rt_queue.append(RealTimeRequest(requests[index]))
            else:
                queue.append(Request(requests[index]))
            index += 1
            added = True

        if added:
            rt_queue.sort()
            sorted_queue = sorted(queue)
            qindex = binary_search(sorted_queue, position, forward or forward is None)
            rtqindex = binary_search(rt_queue, position, forward or forward is None)

        while 0 <= rtqindex < len(rt_queue) and rt_queue[rtqindex].location == position:
            if rt_queue[rtqindex].active(movement):
                real_time_data.append(rt_queue[rtqindex].real_time_data(movement))
            else:
                unrealized_count += 1
            if rt_queue[rtqindex] == req:
                req = None
            rt_queue.pop(rtqindex)
            if not forward:
                rtqindex -= 1

        while 0 <= qindex < len(queue) and sorted_queue[qindex].location == position:
            waiting_times.append(sorted_queue[qindex].waiting_time(movement))
            queue.remove(sorted_queue[qindex])
            sorted_queue.pop(qindex)
            if not forward:
                qindex -= 1

        if req is None and len(rt_queue) > 0:
            sorted_rt_queue = sorted(rt_queue, key=delta_func(position))
            while len(rt_queue) > 0 and not (req := sorted_rt_queue[0]).can_do(movement, position):
                rt_queue.remove(req)
                unrealized_count += 1
                sorted_rt_queue.pop(0)
            if len(rt_queue) > 0:
                forward = req.location > position
                rtqindex = binary_search(rt_queue, position, forward)
                qindex = binary_search(sorted_queue, position, forward)

    return queue, index, position, movement, waiting_times, forward, unrealized_count, real_time_data


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


def delta_func(position):
    return lambda x: - abs(position - x.location)
