from typing import Optional

import numpy as np
from matplotlib import pyplot as plt

from fcfs import fcfs
from rr import rr
from sjf import sjf
from util import process_entry, generate_processes

n: int = 100000  # process count
max_delta: int = 100
max_len: int = 50
window_length = 10

processes: list[process_entry] = generate_processes(n, max_delta, max_len)

data: dict[str, tuple[list[int], list[int], int, Optional[list[int]], int]] = {}

for f in [fcfs, sjf, rr]:
    data[f.__name__] = f(processes, window=window_length)


for name, (queue_times, _, contexts, _, x) in data.items():
    plt.plot(np.arange(len(queue_times)), queue_times)
    plt.suptitle(f'context changes = {contexts}', x=0.35, y=0.75)
    plt.title(name.upper() + " - waiting time")
    plt.vlines(x, 0, max(queue_times), colors='r')
    plt.show()

for name, (_, submit_times, contexts, _, x) in data.items():
    plt.plot(np.arange(len(submit_times)), submit_times)
    plt.title(name.upper() + " - complection time")
    plt.vlines(x, 0, max(submit_times), colors='r')
    plt.show()

next_window_waiting_times: list[int] = data['rr'][3]
x = data['rr'][4]
plt.vlines(x, 0, max(next_window_waiting_times), colors='r')
plt.plot(np.arange(len(next_window_waiting_times)), next_window_waiting_times)
plt.title('RR - next window time')
plt.show()
