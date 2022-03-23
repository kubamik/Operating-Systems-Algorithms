import typing
from collections import namedtuple
import random

import numpy as np


process_entry: typing.Type['process_entry'] = namedtuple('process_entry', 'arrival_time length')


class Process:
    _start: typing.Optional[int] = None
    _last_end: typing.Optional[int] = None

    def __init__(self, entry: process_entry):
        self.arrival: int = entry.arrival_time
        self.length: int = entry.length
        self.remaining: int = entry.length

    def resume(self, time: int) -> int:
        last_end = self._last_end
        self._last_end = time
        if self._start is None:
            self._start = time
            return time - self.arrival
        return time - last_end

    def do(self, time_amount: typing.Optional[int] = None) -> int:
        if time_amount is None:
            time_amount = self.length
        if time_amount > self.remaining:
            time_amount = self.remaining
        self.remaining -= time_amount
        self._last_end += time_amount

        return time_amount

    def time_until_now(self, time: int) -> int:
        return time - self.arrival

    def is_done(self) -> bool:
        return self.remaining <= 0

    def is_started(self):
        return self._start is not None

    def __lt__(self, other):
        if self.length != other.length:
            return self.length < other.length
        return self.arrival < other.arrival


def generate_processes(n: int, max_delta: int, max_len: int) -> list[process_entry]:
    processes: list[process_entry] = []
    before_time = 0
    for _ in range(n):
        processes.append(
            process_entry(before_time + random.randint(0, max_delta), round(np.random.beta(5, 5) * max_len)))
        before_time = processes[-1].arrival_time

    return processes


def serial_generate_processes(n: int, data: list[tuple[float, float, int, int]]) -> list[process_entry]:
    processes: list[process_entry] = []
    steps = len(data)
    data_it = iter(data + [data[-1]])
    alpha, beta, max_delta, max_len = 0, 0, 0, 0
    before_time = 0
    for i in range(n):
        if i % (n // steps) == 0:
            alpha, beta, max_delta, max_len = next(data_it)
        processes.append(
            process_entry(before_time + round(np.random.beta(2, 2) * max_delta),
                          round(np.random.beta(alpha, beta) * max_len)))

        before_time = processes[-1].arrival_time

    return processes
