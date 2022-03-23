from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from fcfs import fcfs
from rr import rr
from sjf import sjf
from util import process_entry, serial_generate_processes

simulations = [
    # (name, n, k [(alpha, beta, max_delta, max_len), ...]),
    ("medium", 10000, 10, [(3, 4, 20, 50)]),
    ("long start", 10000, 10, [(4, 1, 40, 50), (3, 4, 50, 50)]),
    ("long breaks", 10000, 10, [(3, 4, 50, 50)]),
    ("from long to short", 10000, 10, [(4, 1, 150, 150), (2, 4, 50, 100), (3, 4, 25, 50)]),
    ("from long to shorter", 10000, 10, [(4, 1, 150, 150), (2, 4, 40, 75), (3, 4, 15, 25)]),
    ("SJF starving - long", 100000, 10, [(3, 4, 40, 50)]),
    ("SJF starving - short", 100000, 10, [(3, 4, 45, 50)]),
    ("very dense", 10000, 15, [(7, 1, 10, 30)]),
    ("very long breaks", 100000, 5, [(3, 4, 100, 20)])
]

for name, n, k, data in simulations:
    processes: list[process_entry] = serial_generate_processes(n, data)
    results: dict[str, tuple[list[int], list[int], int, Optional[list[int]], int]] = {}
    for f in [fcfs, sjf, rr]:
        results[f.__name__] = f(processes, window=k)

    texts = [[], [], []]
    fig, ax = plt.subplots(3, 3, figsize=(30, 30))
    fig.suptitle(f"{name} - n={n}, k={k}", fontsize=30, y=0.93)
    for i, (alg_name, (wait, complete, contexts, windows, stop)) in enumerate(results.items()):
        texts[i].append(f"{np.mean(wait):.2f}")
        texts[i].append(f"{np.mean(complete):.2f}")
        texts[i].append(contexts)
        if windows is not None:
            texts[i].append(f"{np.mean(windows):.2f}")
        else:
            texts[i].append('-')
        texts[i].append(max(complete))

        ax[0][i].plot(np.arange(n), wait, label='waiting time')
        ax[0][i].set_title(alg_name.upper() + ' - waiting time')
        ax[0][i].vlines(stop, 0, max(wait), colors='r')
        ax[0][i].set_xlabel("finished process count")
        ax[0][i].set_ylabel("time")

        ax[1][i].plot(np.arange(n), complete, label='completion time')
        ax[1][i].set_title(alg_name.upper() + ' - completion time')
        ax[1][i].vlines(stop, 0, max(complete), colors='r')
        ax[1][i].set_xlabel("finished process count")
        ax[1][i].set_ylabel("time")

        if windows is not None:
            ax[2][i].plot(np.arange(len(windows)), windows, label='next window waitng time')
            ax[2][i].set_title(alg_name.upper() + ' - next window waiting time')
            ax[2][i].set_xlabel("window number")
            ax[2][i].set_ylabel("time")
        else:
            ax[2][i].set_axis_off()

    plt.show()

    fig, ax = plt.subplots(dpi=300)
    fig.suptitle(f"{name} - n={n}, k={k}", fontsize=15, y=0.93)
    ax.table(cellText=texts, loc='center', colLabels=['avg waiting time', 'avg completion time', 'context changes',
                                                      'avg next window waiting time', 'max complection time'], rowLabels=['FCFS', 'SJF', 'RR'],
             rowColours=['palegreen']*3, colColours=['palegreen']*5)
    ax.set_axis_off()
    plt.show()
