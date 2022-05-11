from util import Request, rt_request_entry


def sstf(requests, _, queue=None, index=0, position=0, movement=0, waiting_times=None, cycles=None,
         idle_time=0, *__, **___):
    if queue is None:
        queue = list()
    if waiting_times is None:
        waiting_times = list()

    forward = None
    req = None

    times = []

    while index != len(requests) or len(queue) > 0:
        if forward is not None:
            position += (not forward) * (-2) + 1
            movement += 1

        if len(queue) == 0:
            idle_time += requests[index].arrival - movement
            movement = requests[index].arrival
        while index < len(requests) and requests[index].arrival <= movement:
            if isinstance(requests[index], rt_request_entry):
                return queue, index, position, movement, waiting_times, cycles, idle_time
            queue.append(Request(requests[index]))
            index += 1

        if req is None:
            queue.sort(key=distance_func(position))
            req = queue[0]
            forward = req.location > position

        while req is not None and req.location == position:
            times.append(movement)
            waiting_times.append(req.waiting_time(movement))
            queue.pop(0)
            queue.sort(key=distance_func(position))
            req = queue[0] if len(queue) > 0 else None
            forward = req.location > position if len(queue) > 0 else None

    return queue, index, position, movement-idle_time, waiting_times, cycles, idle_time


def distance_func(position):
    return lambda x: abs(x.location - position)
