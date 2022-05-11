from util import request_entry, generate_requests
from simulation import simulate, simulate_rt

tests = [
    ("Starving", 1001, [request_entry(0, 1000), request_entry(0, 50)] + generate_requests(100, 1000, 20, 3, 2)),
    ("Random", 101, generate_requests(100, 1000, 20, 2, 2)),
    ("Long breaks", 1001, generate_requests(1000, 5000, 100, 10, 4)),
    ("Short breaks", 1001, generate_requests(1000, 5000, 10, 4, 10)),
    ("Very long breaks", 1001, generate_requests(1000, 5000, 1000, 2, 2)),
]

rt_tests = [
    ("10 % real time", 1001, generate_requests(1000, 5000, 50, 2, 2, 0.1, 1, 1000)),
    ("10 % real time, long deadline", 1001, generate_requests(1000, 5000, 50, 2, 2, 0.1, 1, 1500)),
    ("10 % real time, long breaks", 1001, generate_requests(1000, 5000, 100, 2, 2, 0.1, 1, 1000)),
    ("10 % real time, very long breaks", 1001, generate_requests(1000, 5000, 1000, 2, 2, 0.1, 1, 1000)),
    ("20 % real time", 1001, generate_requests(1000, 5000, 50, 2, 2, 0.2, 1, 1000)),
    ("1 % real time, short deadline", 1001, generate_requests(1000, 5000, 50, 2, 2, 0.01, 1, 500)),
    ("1 % real time, longer deadline", 1001, generate_requests(1000, 5000, 50, 2, 2, 0.01, 1, 1000)),
]


if __name__ == '__main__':
    print("Normal simulation:")
    for name, size, requests in tests:
        simulate(name, requests, size)

    print("\nReal time simulation:")
    for name, size, requests in rt_tests:
        simulate_rt(name, requests, size)
