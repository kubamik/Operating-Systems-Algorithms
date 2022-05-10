from util import RealTimeRequest, rt_request_entry, Request


def edf(requests, _, queue, index, position, movement, *args, unrealized_count=0, real_time_data=None):
    if real_time_data is None:
        real_time_data = []

    rt_queue = [RealTimeRequest(requests[index])]
    index += 1
    req = rt_queue[0]
    forward = None if req.location == position else req.location > position

    while len(rt_queue) > 0:
        if forward is not None:
            position += (not forward) * (-2) + 1
            movement += 1
        while index < len(requests) and requests[index].arrival <= movement:
            if isinstance(requests[index], rt_request_entry):
                rt_queue.append(RealTimeRequest(requests[index]))
            else:
                queue.append(Request(requests[index]))
            index += 1

        while req is not None and (req.location == position or not req.active(movement)):
            if req.active(movement):
                real_time_data.append(req.real_time_data(movement))
            else:
                unrealized_count += 1
            rt_queue.pop(0)
            rt_queue.sort(key=lambda x: x.deadline)
            req = rt_queue[0] if len(rt_queue) > 0 else None
            forward = req.location > position if len(rt_queue) > 0 else None

    return queue, index, position, movement, *args, None, unrealized_count, real_time_data
