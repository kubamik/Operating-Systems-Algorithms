from matplotlib import pyplot as plt
import numpy as np

from first_strategy import first
from second_strategy import second
from third_strategy import third
from generator import generate


SIMULATIONS = [
    (50, 50, 25, 25, [(20, 30, 30, 40, 1, 10, 200, 300, 7), (50, 80, 10, 100, 20, 40, 50, 75, 3)]),
    (50, 60, 49, 40, [(20, 30, 20, 80, 10, 15, 300, 300, 5), (50, 80, 10, 100, 20, 40, 0, 0, 5)]),
    (50, 60, 20, 20, [(10, 50, 10, 50, 1, 30, 100, 150, 1)]),
    (50, 90, 20, 51, [(40, 50, 45, 50, 20, 30, 100, 150, 1)]),
    (50, 25, 49, 75, [(40, 50, 25, 25, 5, 10, 500, 600, 1), (40, 50, 25, 25, 5, 30, 0, 0, 4)]),
]

stats = []


def simulate(n, gen_strategy, p, z, r):
    processes = generate(n, gen_strategy)
    for i, strategy in enumerate([first, second, third]):
        symbol = f'{i+1}.'
        loads, migrations, questions = strategy(n, processes, p, z, r)
        std = np.std(loads, axis=0)
        plt.hist(np.mean(loads, axis=1), bins=n // 5, rwidth=0.9)
        plt.title(f'{symbol} avg load for processor histogram')
        plt.show()

        stats.append((symbol, migrations, questions, np.mean(std)))
        plt.errorbar(range(len(loads[0])), np.mean(loads, axis=0), yerr=np.std(loads, axis=0), ecolor='k')
        plt.title(symbol + ' avg load')
        plt.show()

        plt.bar(range(n), [len([l for l in load if l > 100]) for load in loads])
        plt.title(symbol + ' overload time by processors')
        plt.show()
    print()


def main():
    for n, p, z, r, gen in SIMULATIONS:
        simulate(n, gen, p, z, r)
        print('|', "-" * 4, '|', "-" * 20, '|', "-" * 20, '|', '-' * 20, '|', sep='')
        print('|{:^4}|{:^20}|{:^20}|{:^20}|'.format('i', 'Migrations', 'Questions', 'Avg. stddev'))
        print('|', "-" * 4, '|', "-" * 20, '|', "-" * 20, '|', '-' * 20, '|', sep='')
        for symbol, migrations, questions, std in stats:
            print('|{:^4}|{:^20}|{:^20}|{:^20.5f}|'.format(symbol, migrations, questions, np.mean(std)))
            print('|', "-" * 4, '|', "-" * 20, '|', "-" * 20, '|', '-' * 20, '|', sep='')
        stats.clear()
        print()


if __name__ == '__main__':
    main()