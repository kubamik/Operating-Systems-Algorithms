import random
from collections import namedtuple

import numpy as np


def generate_requests(size, count, max_time_step, alpha, beta, real_time_factor=0, min_deadline=1, max_deadline=1):
    requests = list()
    time = 0
    for _ in range(count):
        time += int(np.round(np.random.beta(alpha, beta) * max_time_step))
        location = random.randint(0, size - 1)
        if random.random() < real_time_factor:
            deadline = int(np.random.beta(10, 4) * (max_deadline - min_deadline) + min_deadline)
            requests.append(rt_request_entry(time, location, deadline))
        else:
            requests.append(request_entry(time, location))

    return requests


def run(requests, size, algorithm):
    _, _, _, movement, waiting_times, cycles, *_ = algorithm(requests, size)
    return movement, waiting_times, cycles


def run_real_time(requests, size, normal_algorithm, real_time_algorithm):
    queue = list()
    index = 0
    movement = 0
    position = 0
    waiting_times = list()
    cycles = None
    args = list()
    unrealized_count = 0
    real_time_data = list()
    forward = None
    while index < len(requests) or len(queue) > 0:
        queue, index, position, movement, waiting_times, cycles, *_ = normal_algorithm(
            requests, size, queue, index, position, movement, waiting_times, cycles, *args, forward=forward)
        if index < len(requests):
            queue, index, position, movement, waiting_times, forward, unrealized_count, real_time_data = \
                real_time_algorithm(
                    requests, size, queue, index, position, movement, waiting_times,
                    unrealized_count=unrealized_count, real_time_data=real_time_data)
    return movement, waiting_times, cycles, unrealized_count, real_time_data


request_entry = namedtuple('request_entry', 'arrival location')
rt_request_entry = namedtuple('real_time_request_entry', 'arrival location deadline')


class Request:
    def __init__(self, req):
        self.arrival = req.arrival
        self.location = req.location

    def waiting_time(self, current_time):
        return current_time - self.arrival

    def __str__(self):
        return f'arr={self.arrival} loc={self.location}'

    def __lt__(self, other):
        if self.location != other.location:
            return self.location < other.location
        return self.arrival < other.arrival


class RealTimeRequest(Request):
    def __init__(self, req):
        super().__init__(req)
        self.deadline = req.deadline

    def delta(self, time, position):
        return self.deadline - abs(self.location - position) - time + self.arrival

    def can_do(self, time, position):
        return self.delta(time, position) >= 0

    def active(self, time):
        return time <= self.deadline + self.arrival

    def real_time_data(self, time):
        return self.deadline, self.waiting_time(time)

    def __str__(self):
        return f'arr={self.arrival} loc={self.location} dead={self.deadline}'
