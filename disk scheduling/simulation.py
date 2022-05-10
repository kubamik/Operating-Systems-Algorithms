from operator import itemgetter

from fcfs import fcfs
from sstf import sstf
from scan import scan
from c_scan import c_scan
from edf import edf
from fd_scan import fd_scan
from util import run, run_real_time

EDF = """\
\t\t\t\t*****  ****    *****
\t\t\t\t*      *   *   *
\t\t\t\t*****  *    *  *****
\t\t\t\t*      *   *   *
\t\t\t\t*****  ****    *"""

FD_SCAN = """\
\t\t\t\t*****  ****           *****  *****  ******  *     *
\t\t\t\t*      *   *          *      *      *    *  * *   *
\t\t\t\t*****  *    *  *****  *****  *      ******  *  *  *
\t\t\t\t*      *   *              *  *      *    *  *   * *
\t\t\t\t*      ****           *****  *****  *    *  *     *"""


def simulate(name, requests, size):
    def line():
        print('', '-' * 8, '-' * 10, '-' * 16, '-' * 16, '-'*10, sep='|', end='|\n')
    temp = '|{:^8}|{:^10}|{:^16.2f}|{:^16}|{:^10}|'
    print('-' * 70)
    print(name)
    print('Size:\t', size, '\t\tCount:\t', len(requests))
    line()
    print('|{:^8}|{:^10}|{:^16}|{:^16}|{:^10}|'.format('Name', 'Time', 'Avg. wait time', 'Max wait time', 'Cycles'))
    line()
    for algo in [fcfs, sstf, scan, c_scan]:
        mov, times, cycles = run(requests, size, algo)
        name = algo.__name__.upper().replace('_', '-')
        print(temp.format(name, mov, sum(times) / len(times), max(times), str(cycles)))
        line()
    print('\n\n')


def simulate_rt(name, requests, size):
    print('-' * 130)
    print(name)
    print('-'*130)
    print(EDF)
    _simulate_rt(requests, size, edf)
    print(FD_SCAN)
    _simulate_rt(requests, size, fd_scan)
    print('\n\n')


def _simulate_rt(requests, size, rt_algo):
    def line():
        print('', '-' * 8, '-' * 10, '-' * 25, '-' * 16, '-'*10, '-'*26, '-'*26, sep='|', end='|\n')
    temp = '|{:^8}|{:^10}|{:^25.2f}|{:^16}|{:^10}|{:^26}|{:^26.2f}|'
    line()
    print('|{:^8}|{:^10}|{:^25}|{:^16}|{:^10}|{:^26}|{:^26}|'.format('Name', 'Time', 'Normal avg. wait time',
                                                                     'Max wait time', 'Cycles',
                                                                     'Canceled / all real time',
                                                                     'Real time avg. wait time'))
    line()
    for algo in [fcfs, sstf, scan, c_scan]:
        mov, times, cycles, not_realized, real_time_data = run_real_time(requests, size, algo, rt_algo)
        name = algo.__name__.upper().replace('_', '-')
        real_time_times = list(map(itemgetter(1), real_time_data))
        print(temp.format(name, mov, sum(times) / len(times), max(times), str(cycles),
                          str(not_realized) + ' / ' + str(len(real_time_times) + not_realized),
                          len(real_time_data) and sum(real_time_times) / len(real_time_times)))
        line()
