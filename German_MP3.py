from typing import Dict, List, Tuple
import os
import time


class PlacementAlgorithm:
    def __init__(self, memory: List[Dict[str, int]], jobs: List[Dict[str, int]]) -> None:
        self.memory: List[Dict[str, int]] = self.sort(memory)
        self.maximum: int = max([block['size'] for block in memory])
        self.jobs: List[Dict[str, int]] = [
            job for job in jobs if job['size'] <= self.maximum]

    def simulate(self):
        history: List[Dict[str, List[Dict[str, int]]]] = []
        running: List[Dict[str, int]] = [
            None for _ in range(0, len(self.memory))]

        while len(self.jobs) > 0:
            for i in range(0, len(self.jobs)):
                block = self.select_block(self.jobs[i], running)
                if block != -1:
                    running[block] = self.jobs[i].copy()
                    self.jobs[i] = None

            while any([job == None for job in self.jobs]):
                self.jobs.pop(self.jobs.index(None))

            history.append({
                "running": running.copy(),
                "waiting": self.jobs.copy()
            })

            for i in range(0, len(running)):
                if running[i] != None:
                    time = running[i]['time'] - 1
                    if time <= 0:
                        running[i] = None
                    else:
                        running[i]['time'] = time

        return history

    def sort(self):
        raise NotImplementedError()

    def select_block(self, job: Dict[str, int], running: List[Dict[str, int]]):
        for i in range(0, len(self.memory)):
            if self.memory[i]['size'] >= job['size'] and running[i] == None:
                return i
        return -1


class FirstFit(PlacementAlgorithm):
    def sort(self, memory: List[Dict[str, int]]):
        return memory


class WorstFit(PlacementAlgorithm):
    def sort(self, memory: List[Dict[str, int]]):
        return sorted(memory, key=lambda x: x['size'], reverse=True)


class BestFit(PlacementAlgorithm):
    def sort(self, memory: List[Dict[str, int]]):
        return sorted(memory, key=lambda x: x['size'])


class Evaluator:
    def __init__(self, memory: List[Dict[str, int]], history: List[Dict[str, List[Dict[str, int]]]]) -> None:
        self.memory = memory
        self.history = history

    def compute_metrics(self):
        throughput: List[int] = []
        storage_utilization: List[Tuple[int, int]] = []
        waiting_queue_length: List[int] = []
        waiting_time_in_queue: List[int] = []
        internal_fragmentation: List[int] = []

        os.system("cls")
        for unit in self.history:
            throughput.append(len(unit['running']))
            storage_utilization.append((sum([1 for job in unit['running'] if job != None]), sum(
                [1 for job in unit['running'] if job == None])))
            waiting_queue_length.append(len(unit['waiting']))
            waiting_time_in_queue.append(
                min([job['time'] for job in unit['running'] if job != None]))
            internal_fragmentation.append(sum(
                [self.memory[i]['size'] - unit['running'][i]['size'] for i in range(0, len(unit['running'])) if unit['running'][i] != None]))

        max_throughput = max(throughput)
        average_throughput = sum(throughput)/len(throughput)
        min_throughput = min(throughput)

        partitions_used = [e[0] for e in storage_utilization]
        max_percentage_partitions_used = max(partitions_used)
        average_percentage_partitions_used = sum(
            partitions_used)/len(storage_utilization)
        min_percentage_partitions_used = min(partitions_used)

        partitions_unused = [e[1] for e in storage_utilization]
        max_percentage_partitions_unused = max(partitions_unused)
        average_percentage_partitions_unused = sum(
            partitions_unused)/len(storage_utilization)
        min_percentage_partitions_unused = min(partitions_unused)

        average_waiting_queue_length = sum(
            waiting_queue_length)/len(waiting_queue_length)

        max_waiting_time_queue = max(waiting_time_in_queue)
        average_waiting_time_queue = sum(
            waiting_time_in_queue)/len(waiting_time_in_queue)
        min_waiting_time_queue = min(waiting_time_in_queue)

        max_internal_fragmentation = max(internal_fragmentation)
        average_internal_fragmentation = sum(
            internal_fragmentation)/len(internal_fragmentation)
        min_internal_fragmentation = min(
            [leftover for leftover in internal_fragmentation if leftover >= 0])

        print(
            """
####################################################################
                        Performance Metrics
        
            Max Throughput: {:.2f}
            Average Throughput: {:.2f}
            Min Throughput: {:.2f}

            Max Percentage of Partitions Used: {:.2f}
            Average Percentage of Partitions Used: {:.2f}
            Min Percentage of Partitions Used: {:.2f}

            Max Percentage of Partitions Used: {:.2f}
            Average Percentage of Partitions Not Used: {:.2f}
            Min Percentage of Partitions Used: {:.2f}

            Average Waiting Queue Length: {:.2f}

            Max Waiting Time in Queue: {:.2f}
            Average Waiting Time in Queue: {:.2f}
            Min Waiting Time in Queue: {:.2f}

            Max Total Internal Fragmentation: {:.2f}
            Average Total Internal Fragmentation: {:.2f}
            Min Total Internal Fragmentation: {:.2f}
        """.format(
                max_throughput,
                average_throughput,
                min_throughput,
                max_percentage_partitions_used,
                average_percentage_partitions_used,
                min_percentage_partitions_used,
                max_percentage_partitions_unused,
                average_percentage_partitions_unused,
                min_percentage_partitions_unused,
                average_waiting_queue_length,
                max_waiting_time_queue,
                average_waiting_time_queue,
                min_waiting_time_queue,
                max_internal_fragmentation,
                average_internal_fragmentation,
                min_internal_fragmentation
            ))


def main():
    while True:
        os.system("cls")
        memory = [
            {"id": 1, "size": 9500},
            {"id": 2, "size": 7000},
            {"id": 3, "size": 4500},
            {"id": 4, "size": 8500},
            {"id": 5, "size": 3000},
            {"id": 6, "size": 9000},
            {"id": 7, "size": 1000},
            {"id": 8, "size": 5500},
            {"id": 9, "size": 1500},
            {"id": 10, "size": 500},
        ]
        jobs = [
            {"id": 1, "time": 5, "size": 5760},
            {"id": 2, "time": 4, "size": 4190},
            {"id": 3, "time": 8, "size": 3290},
            {"id": 4, "time": 2, "size": 2030},
            {"id": 5, "time": 2, "size": 2550},
            {"id": 6, "time": 6, "size": 6990},
            {"id": 7, "time": 8, "size": 8940},
            {"id": 8, "time": 10, "size": 740},
            {"id": 9, "time": 7, "size": 3930},
            {"id": 10, "time": 6, "size": 6890},
            {"id": 11, "time": 5, "size": 6580},
            {"id": 12, "time": 8, "size": 3820},
            {"id": 13, "time": 9, "size": 9140},
            {"id": 14, "time": 10, "size": 420},
            {"id": 15, "time": 10, "size": 220},
            {"id": 16, "time": 7, "size": 7540},
            {"id": 17, "time": 3, "size": 3210},
            {"id": 18, "time": 1, "size": 1380},
            {"id": 19, "time": 9, "size": 9850},
            {"id": 20, "time": 3, "size": 3610},
            {"id": 21, "time": 7, "size": 7540},
            {"id": 22, "time": 2, "size": 2710},
            {"id": 23, "time": 8, "size": 8390},
            {"id": 24, "time": 5, "size": 5950},
            {"id": 25, "time": 10, "size": 760},
        ]
        command: str = (input(
            """
####################################################################
            Memory Management and Allocation Strategies
        
        Commands:
        
            1. Use First-Fit
            2. Use Worst-Fit
            3. Use Best-Fit
####################################################################
        Input: """
        ))
        os.system("cls")
        if command == '1':
            history = FirstFit(memory.copy(), jobs.copy()).simulate()
            Evaluator(memory.copy(), history).compute_metrics()
        elif command == '2':
            history = WorstFit(memory.copy(), jobs.copy()).simulate()
            Evaluator(memory.copy(), history).compute_metrics()
        elif command == '3':
            history = BestFit(memory.copy(), jobs.copy()).simulate()
            Evaluator(memory.copy(), history).compute_metrics()
        else:
            break
        time.sleep(3)


if __name__ == '__main__':
    main()
