import numpy as np
from matplotlib import pyplot as plt

from fcfs import fcfs
from rr import rr
from sjf import sjf
from util import process_entry, serial_generate_processes

simulations = [
    # (name, n, k [(alpha, beta, max_delta, max_len), ...]),
    ("short breaks", 10000, [(3, 4, 20, 50)]),
    ("medium breaks", 10000, [(3, 4, 40, 50)])
]

for name, n, data in simulations:
    k_tries = [1, 3, 5, 10, 15, 25, 35, 50]
    
    processes: list[process_entry] = serial_generate_processes(n, data)
    texts = [list() for _ in range(len(k_tries)+2)]
    
    # FCFS
    waiting_times, complete_times, context_changes, _, stop = fcfs(processes)
    plt.plot(np.arange(len(waiting_times)), waiting_times, label="waiting time")
    plt.suptitle(f"context_changes: {context_changes}", x=0.35, y=0.75)
    
    plt.plot(np.arange(len(complete_times)), complete_times, label="until complection time")
    plt.vlines(stop, 0, max(complete_times), colors='r')
    
    texts[0].append(f"{np.mean(waiting_times):.2f}")
    texts[0].append(f"{np.mean(complete_times):.2f}")
    texts[0].append(context_changes)
    texts[0].append(' ')
    texts[0].append(max(complete_times))
    
    plt.xlabel("finished process count")
    plt.ylabel("time")
    plt.title("FCFS")
    plt.legend()
    plt.show()
    
    
    # SJF
    waiting_times, complete_times, context_changes, _, stop = sjf(processes)
    plt.plot(np.arange(len(waiting_times)), waiting_times, label="waiting time")
    
    plt.suptitle(f"context_changes: {context_changes}", x=0.35, y=0.75)
    plt.vlines(stop, 0, max(complete_times), colors='r')
    
    texts[1].append(f"{np.mean(waiting_times):.2f}")
    texts[1].append(f"{np.mean(complete_times):.2f}")
    texts[1].append(context_changes)
    texts[1].append(' ')
    texts[1].append(max(complete_times))
    
    plt.xlabel("finished process count")
    plt.ylabel("time")
    plt.plot(np.arange(len(complete_times)), complete_times, label="until complection time")
    plt.title("SJF")
    plt.legend()
    plt.show()
    
    # RR
    for i, k in enumerate(k_tries):
        waiting_times, complete_times, context_changes, next_window_time, stop = rr(processes, window=k)
    
        plt.suptitle(f"context_changes: {context_changes}", x=0.35, y=0.75)
        plt.vlines(stop, 0, max(complete_times), colors='r')
        
        texts[i+2].append(f"{np.mean(waiting_times):.2f}")
        texts[i+2].append(f"{np.mean(complete_times):.2f}")
        texts[i+2].append(context_changes)
        texts[i+2].append(f"{np.mean(next_window_time):.2f}")
        texts[i+2].append(max(complete_times))
        
        plt.xlabel("finished process count")
        plt.ylabel("time")
    
        plt.plot(np.arange(len(complete_times)), complete_times, label="until complection time")
        plt.plot(np.arange(len(waiting_times)), waiting_times, label="waiting time")
        
        plt.title(f"k={k}")
        plt.legend()
        plt.show()
        
        plt.xlabel("window number")
        plt.ylabel("time")
        plt.plot(np.arange(len(next_window_time)), next_window_time, label="next window time")
        plt.title(f"k={k} - next window time")
        plt.show()
        
    fig, ax = plt.subplots(dpi=300)
    fig.suptitle(f"{name} k-variety - n={n}", fontsize=15, y=0.93)
    print(['FCFS', 'SJF'] + [f'RR - k={k}' for k in k_tries])
    print(len(texts))
    print(['palegreen']*len(texts))
    ax.table(cellText=texts, loc='center', 
             colLabels=['avg waiting time', 'avg completion time', 
                        'context changes', 'avg next window waiting time', 
                        'max complection time'],
             rowLabels=['FCFS', 'SJF'] + [f'RR - k={k}' for k in k_tries],
             rowColours=['palegreen']*len(texts), colColours=['palegreen']*5)
    ax.set_axis_off()
    plt.show()
