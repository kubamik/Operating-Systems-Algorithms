import random

from utils import Processor


def third(n, processes, P, _, R):
    proc = [Processor(i, p) for i, p in enumerate(processes)]
    proc_set = set(proc)
    time = 0
    migrations = 0
    questions = 0
    loads = [list() for _ in range(n)]

    while not all(proc[i].end() for i in range(n)):
        new_processes = [(c, p) for p in proc if (c := p.step(time)) is not None]
        for process, p in new_processes:
            if p.calculate_load() < P:
                p.add_process(process)
                continue
            to_ask = list(proc_set - {p})
            random.shuffle(to_ask)
            for q in to_ask:
                questions += 1
                if q.calculate_load() < P:
                    migrations += 1
                    q.add_process(process)
                    break
            else:
                p.add_process(process)

        for p in proc:
            if p.calculate_load() < R:
                other_proc = random.sample(list(proc_set - {p}), k=n-1)
                for q in other_proc:
                    questions += 1
                    if q.calculate_load() > P:
                        migrations += 1
                        p.add_process(q.remove_largest_process())
                        break

        for i, p in enumerate(proc):
            loads[i].append(p.calculate_load())

        time += 1

    return loads, migrations, questions
