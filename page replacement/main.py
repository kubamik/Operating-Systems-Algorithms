from fifo import fifo
from optimal import opt
from lru import lru
from approx_lru import approx_lru
from rand import rand
from generator import generate

simulations = [
{
        "name": "First",
        "npages": 6,
        "nframes": 4,
        "ncalls": 10000,
        "min_group_size": 3,
        "max_group_size": 5,
        "min_group_length": 10,
        "max_group_length": 50,
    },
    {
        "name": "Second",
        "npages": 20,
        "nframes": 10,
        "ncalls": 10000,
        "min_group_size": 2,
        "max_group_size": 10,
        "min_group_length": 10,
        "max_group_length": 50,
    },
    {
        "name": "Larger local group than frames",
        "npages": 20,
        "nframes": 7,
        "ncalls": 10000,
        "min_group_size": 2,
        "max_group_size": 12,
        "min_group_length": 10,
        "max_group_length": 40,
    },
    {
        "name": "Low frames",
        "npages": 20,
        "nframes": 2,
        "ncalls": 10000,
        "min_group_size": 2,
        "max_group_size": 5,
        "min_group_length": 10,
        "max_group_length": 100,
    },
    {
        "name": "Long local groups",
        "npages": 20,
        "nframes": 10,
        "ncalls": 10000,
        "min_group_size": 7,
        "max_group_size": 10,
        "min_group_length": 100,
        "max_group_length": 200,
    },
    {
        "name": "Short local groups",
        "npages": 20,
        "nframes": 10,
        "ncalls": 10000,
        "min_group_size": 7,
        "max_group_size": 12,
        "min_group_length": 12,
        "max_group_length": 20,
    },
    {
        "name": "Large test",
        "npages": 50,
        "nframes": 10,
        "ncalls": 100000,
        "min_group_size": 7,
        "max_group_size": 12,
        "min_group_length": 500,
        "max_group_length": 1000,
    }
]

if __name__ == '__main__':
    algos = [fifo, opt, lru, approx_lru, rand]
    for simulation in simulations:
        print(simulation['name'])
        calls = generate(**simulation)

        print("|", "-" * 12, "|", "-" * 12, "|", "-" * 12, "|", "-" * 12, "|", "-" * 12, "|", "-" * 12, "|", sep="")
        print("|{:^12}|{:^12}|{:^12}|{:^12}|{:^12}|{:^12}|".format(
            "Algorithm", *[a.__name__.upper().replace('_', '-') for a in algos]))
        print("|", "-" * 12, "|", "-"*12, "|", "-"*12, "|", "-"*12, "|", "-"*12, "|", "-"*12, "|", sep="")
        print("|{:^12}|".format("Faults"), end="")

        for a in algos:
            print("{:^12}".format(a(simulation['npages'], simulation['nframes'], calls)), end='|')

        print("\n", "|",  "-" * 12, "|", "-"*12, "|", "-"*12, "|", "-"*12, "|", "-"*12, "|", "-"*12, "|",
              sep="", end="\n\n\n")
