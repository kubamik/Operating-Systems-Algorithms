import random

from utils import Processor


def first(n, processes, P, Z, _):
    proc = [Processor(i, p) for i, p in enumerate(processes)]
    proc_set = set(proc)
    time = 0
    migrations = 0
    questions = 0
    loads = [list() for _ in range(n)]

    while not all(proc[i].end() for i in range(n)):
        new_processes = [(c, p) for p in proc if (c := p.step(time)) is not None]
        for process, p in new_processes:
            to_ask = random.sample(proc_set - {p}, Z)
            for q in to_ask:
                questions += 1
                if q.calculate_load() < P:
                    migrations += 1
                    q.add_process(process)
                    break
            else:
                p.add_process(process)

        for i, p in enumerate(proc):
            loads[i].append(p.calculate_load())

        time += 1

    return loads, migrations, questions
