from collections import namedtuple


class Processor:

    def __init__(self, i, processes):
        self.id = i
        self.current_processes = list()
        self.processes = processes
        self.idx = 0

    def calculate_load(self):
        return sum(process.weight for process in self.current_processes)

    def add_process(self, process):
        self.current_processes.append(process)

    def remove_processes(self, time):
        for process in self.current_processes:
            if process.start_time + process.duration <= time:
                self.current_processes.remove(process)

    def remove_largest_process(self):
        proc = max(self.current_processes, key=lambda p: p.weight)
        self.current_processes.remove(proc)
        return proc

    def step(self, time):
        self.remove_processes(time)
        if self.idx < len(self.processes) and self.processes[self.idx].start_time == time:
            self.idx += 1
            return Process.from_entry(self.processes[self.idx - 1])
        return None

    def end(self):
        return self.idx == len(self.processes)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f"Processor {self.id}"


class Process:
    def __init__(self, weight, start_time, duration):
        self.weight = weight
        self.start_time = start_time
        self.duration = duration

    @classmethod
    def from_entry(cls, entry):
        return cls(entry.weight, entry.start_time, entry.duration)

    def __repr__(self):
        return f"{self.weight} @ {self.start_time} for {self.duration}"


process_entry = namedtuple('process_entry', 'weight, start_time, duration')
