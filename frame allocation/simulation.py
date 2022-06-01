from generator import generate
from equal import equal
from proportional import proportional
from pff import pff
from working_sets import working_sets

SIMULATIONS = [
    {
        'name': 'first',
        'process_data': [(10, 1000), (15, 1000), (10, 1000), (12, 1000), (10, 1000), (13, 1000),
                         (15, 1000), (13, 1000), (12, 1000), (15, 1000)],
        'nframes': 50,
        'min_group_size': 3,
        'max_group_size': 5,
        'min_group_length': 100,
        'max_group_length': 100,
        'l': 0.02,
        'u': 0.15,
        'pfft': 50,
        'c': 100,
        'wst': 200,
    },
    {
        'name': 'second',
        'process_data': [(10, 1000), (15, 1000), (10, 1000), (12, 1000), (10, 1000), (13, 1000),
                         (15, 1000), (13, 1000), (12, 1000), (15, 1000)] * 3,
        'nframes': 125,
        'min_group_size': 3,
        'max_group_size': 6,
        'min_group_length': 30,
        'max_group_length': 100,
        'l': 0.2,
        'u': 0.6,
        'pfft': 40,
        'c': 50,
        'wst': 200,
    },
    {
        'name': 'third',
        'process_data': [(15, 1000)] * 10,
        'nframes': 60,
        'min_group_size': 3,
        'max_group_size': 10,
        'min_group_length': 30,
        'max_group_length': 100,
        'l': 0.02,
        'u': 0.1,
        'pfft': 40,
        'c': 100,
        'wst': 200,
    },
{
        'name': 'fourth',
        'process_data': [(5, 100), (15, 1000), (10, 1000), (6, 200), (10, 200), (13, 1000), (30, 1000)],
        'nframes': 50,
        'min_group_size': 3,
        'max_group_size': 7,
        'min_group_length': 30,
        'max_group_length': 100,
        'l': 0.02,
        'u': 0.1,
        'pfft': 40,
        'c': 100,
        'wst': 200,
    },
]


def main():
    for simulation in SIMULATIONS:
        print('=' * 80, '\n\n')
        print(simulation['name'].upper() + ':\n')
        calls = generate(**simulation)
        process_data = simulation.pop('process_data')
        for algo in [equal, proportional, pff, working_sets]:
            faults, history, pauses = algo(calls=calls.copy(), process_data=process_data.copy(), **simulation)
            print(f'{algo.__name__.upper()}:')
            print(f'\tPauses: {pauses}')
            print(f'\tFaults: {sum(len(f) for f in faults.values())}')
            for i, f in sorted(faults.items()):
                print(f'\t\tFault {i}: {len(f)}')
            print('\n')


if __name__ == '__main__':
    main()
