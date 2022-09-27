import csv
from queue import Queue


class CsvMan:
    __slots__ = ["input_file", "task_queue"]

    def __init__(self, input_file):
        self.input_file = input_file
        self.task_queue: Queue = Queue()

    def read_input(self):
        csv_file = open(self.input_file, 'r')
        for line in csv_file:
            self.task_queue.put(line.rstrip())

    def is_queue_empty(self):
        return self.task_queue.empty()

    def num_of_items(self):
        return self.task_queue.qsize()
