from typing import Optional

from util import process_entry, Process
from heapq import heappush, heappop, heapify


def sjf(processes: list[process_entry], **_) -> tuple[list[int], list[int], int, Optional[list[int]], int]:
    index: int = 0
    heap = []
    heapify(heap)
    time: int = processes[index].arrival_time
    queueing_times: list[int] = []
    submitting_times: list[int] = []
    context_changes: int = 0
    stop = -1

    while index < len(processes) or len(heap) > 0:
        while index < len(processes) and processes[index].arrival_time <= time:
            heappush(heap, Process(processes[index]))
            index += 1

        if len(heap) == 0:
            time = processes[index].arrival_time
            continue

        process: Process = heappop(heap)
        queueing_times.append(process.resume(time))
        time += process.do()
        submitting_times.append(process.time_until_now(time))
        context_changes += 1
        if index == len(processes) and stop == -1:
            stop = len(queueing_times)
            
    return queueing_times, submitting_times, context_changes, None, stop
