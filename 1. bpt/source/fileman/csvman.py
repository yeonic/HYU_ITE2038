import csv
from queue import Queue


class CsvMan:
    __slots__ = ["input_file", "task_queue"]

    def __init__(self, input_file):
        self.input_file = input_file
        self.task_queue: Queue = Queue()

    def read_input(self):
        csv_file = open(self.input_file, 'r')
        return self.record_input(csv_file)

    def record_input(self, csv_file):
        for line in csv_file:
            self.task_queue.put(line.rstrip())
