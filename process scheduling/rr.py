from typing import Optional

import numpy as np
from matplotlib import pyplot as plt

from util import process_entry, Process


def rr(processes: list[process_entry], **kwargs) -> tuple[list[int], list[int], int, Optional[list[int]], int]:
    index: int = 0
    queue: list = []
    window = kwargs.get('window')
    time: int = processes[index].arrival_time
    queueing_times: list[int] = []
    submitting_times: list[int] = []
    next_window_wating_times: list[int] = []
    context_changes: int = 0
    stop = -1

    queue_index: int = 0
    last_process: Process = None
    while index < len(processes) or len(queue) > 0:
        while index < len(processes) and processes[index].arrival_time <= time:
            queue.append(Process(processes[index]))
            index += 1

        if queue_index >= len(queue):
            queue_index = 0
            i = 0
            while i < len(queue):
                if queue[i].is_done():
                    queue.pop(i)
                    i -= 1
                i += 1
        
        if index == len(processes) and stop == -1:
            stop = len(submitting_times)

        if len(queue) == 0:
            if index >= len(processes):
                break
            time = processes[index].arrival_time
            continue

        process: Process = queue[queue_index]
        
        if not process.is_started():
            resumed_time: int = process.resume(time)
            queueing_times.append(resumed_time)
        else:
            resumed_time: int = process.resume(time)
        next_window_wating_times.append(resumed_time)
        time += process.do(window)
        if process.is_done():
            submitting_times.append(process.time_until_now(time))
        if process != last_process:
            context_changes += 1
        queue_index += 1
        last_process = process
    
    return queueing_times, submitting_times, context_changes, next_window_wating_times, stop
