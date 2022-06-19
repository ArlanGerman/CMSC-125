from typing import Dict, List
import os
import time

from sqlalchemy import true


class Scheduler:
    """
    Returns completion, turnaround, and waiting times
    """

    def __init__(self, processes: Dict[str, List[int]]) -> None:
        self.processes = processes

    def schedule(self) -> List[Dict[str, int]]:
        self.sort()
        burst: int = self.processes[0]['CPU Burst Time']
        turnaround: int = self.compute_turnaround_time(
            burst, self.processes[0]['Arrival'])
        gantt: List[Dict[str, int]] = [
            {
                'Process': self.processes[0]['Process'],
                'Completion Time': burst,
                'Turnaround Time': turnaround,
                'Waiting Time': self.compute_waiting_time(turnaround, burst)
            }
        ]

        for i in range(1, len(self.processes)):
            burst: int = self.processes[i]['CPU Burst Time']
            completion: int = self.compute_completion_time(
                gantt[i - 1]['Completion Time'], burst)
            turnaround: int = self.compute_turnaround_time(
                completion, self.processes[i]['Arrival'])
            gantt.append({
                'Process': self.processes[i]['Process'],
                'Completion Time': completion,
                'Turnaround Time': turnaround,
                'Waiting Time': self.compute_waiting_time(turnaround, burst)
            })

        return gantt

    def sort(self):
        raise NotImplementedError()

    def compute_completion_time(self, burst_time_previous: int, burst_time_current: int) -> int:
        return burst_time_previous + burst_time_current

    def compute_turnaround_time(self, completion_time: int, arrival_time: int) -> int:
        return completion_time - arrival_time

    def compute_waiting_time(self, turnaround_time: int, burst_time: int) -> int:
        return turnaround_time - burst_time


class Reader:
    @staticmethod
    def read(filepath: str, with_header: bool = True) -> List[Dict[str, int]]:
        rows = open(filepath).readlines()

        if len(rows) <= 0:
            raise ValueError("File is empty.s")

        rows = [[element for element in row.strip().split('\t') if element != '']
                for row in rows]
        if with_header:
            rows = rows[1:]

        valid_lengths = [len(row) == 4 for row in rows]
        if not all(valid_lengths):
            raise ValueError("There exists a row not equal to 4 elements.")

        return [
            {
                'Process': int(row[0]),
                'Arrival': int(row[1]),
                'CPU Burst Time': int(row[2]),
                'Priority': int(row[3])
            } for row in rows
        ]


class Reporter:
    @staticmethod
    def report(gantt: List[Dict[str, int]]) -> None:
        print(
            """
####################################################################
                        Gantt Chart
        
            {:<20} {:<20} {:<20} {:<20}""".format('Process', 'Completion Time', 'Turnaround Time', 'Waiting Time'),
            end=''
        )
        length = len(gantt)
        for i in range(0, length):
            print(
                """
            {:<20} {:<20} {:<20} {:<20}""".format(gantt[i]['Process'], gantt[i]['Completion Time'], gantt[i]['Turnaround Time'], gantt[i]['Waiting Time']),
                end=''
            )
        print("\n\n\tAverage Completion Time: %0.2f" %
              (sum([process['Completion Time'] for process in gantt])/length))
        print("\tAverage Turnaround Time: %0.2f" %
              (sum([process['Turnaround Time'] for process in gantt])/length))
        print("\tAverage Waiting Time: %0.2f" %
              (sum([process['Waiting Time'] for process in gantt])/length))


class FCFS(Scheduler):
    def __init__(self, processes: Dict[str, List[int]]) -> None:
        super().__init__(processes)

    def sort(self) -> None:
        return


class SJF(Scheduler):
    def __init__(self, processes: Dict[str, List[int]]) -> None:
        super().__init__(processes)

    def sort(self) -> None:
        self.processes = [self.processes[0], *sorted(
            self.processes[1:], key=lambda e: e['CPU Burst Time'])]


class SRPT(Scheduler):
    def __init__(self, processes: List[Dict[str, int]]) -> None:
        super().__init__(processes)

    def sort(self):
        self.processes: List[Dict[str, int]] = sorted(
            self.processes, key=lambda e: e['Arrival'])
        initial = self.processes.pop(0)
        arrival = self.processes[1]['Arrival']

        self.processes = sorted(
            self.processes, key=lambda e: e['CPU Burst Time'])

        if initial['CPU Burst Time'] > arrival and initial['Arrival'] == 0:
            new_initial = initial.copy()
            new_initial_copy = initial.copy()

            new_initial['CPU Burst Time'] -= self.processes[0]['Arrival']
            new_initial_copy['CPU Burst Time'] = self.processes[0]['Arrival']

            processes = sorted([new_initial, *self.processes],
                               key=lambda e: e['CPU Burst Time'])
            if processes[0]['Process'] == new_initial_copy['Process']:
                self.processes = [initial, *self.processes]
            else:
                self.processes = [new_initial_copy, *processes]


class Priority(Scheduler):
    def __init__(self, processes: List[Dict[str, int]]) -> None:
        super().__init__(processes)

    def sort(self):
        self.processes = sorted(self.processes, key=lambda e: e['Priority'])


class RoundRobin(Scheduler):
    def __init__(self, processes: List[Dict[str, int]], quantum: int) -> None:
        self.processes = processes
        self.quantum = quantum

    def sort(self):
        self.processes: List[Dict[str, int]] = sorted(
            self.processes, key=lambda e: e['Arrival'])
        exceeds = [process['CPU Burst Time'] >
                   self.quantum for process in self.processes]
        while any(exceeds):
            new_process = self.processes[exceeds.index(True)].copy()
            self.processes[exceeds.index(
                True)]['CPU Burst Time'] = self.quantum
            new_process['CPU Burst Time'] -= self.quantum
            self.processes.append(new_process)
            exceeds = [process['CPU Burst Time'] >
                       self.quantum for process in self.processes]


def main():
    os.system("clear")
    filepath: str = input(
        """
####################################################################
        Processor Management and Job Scheduling

    Input path to file: """
    )

    while True:
        os.system("clear")
        processes = Reader.read(filepath, with_header=True)
        command: str = (input(
            """
####################################################################
            Processor Management and Job Scheduling
        
        Commands:
        
            1.  Use FCFS Scheduler
            2.  Use SJF Scheduler
            3.  Use SRPT Scheduler
            4.  Use Priority Scheduler
            5.  Use RoundRobin Scheduler

####################################################################

        Input: """
        ))
        os.system("clear")
        if command == '1':
            gantt = FCFS(processes).schedule()
            Reporter.report(gantt)
        elif command == '2':
            gantt = SJF(processes).schedule()
            Reporter.report(gantt)
        elif command == '3':
            gantt = SRPT(processes).schedule()
            Reporter.report(gantt)
        elif command == '4':
            gantt = Priority(processes).schedule()
            Reporter.report(gantt)
        elif command == '5':
            gantt = RoundRobin(processes, 4).schedule()
            Reporter.report(gantt)
        else:
            break
        time.sleep(3)


if __name__ == '__main__':
    main()
