
from collections import deque
import cupy as cp


class MatrixLinkedList:
    def __init__(self, matrix, dtype=None):
        self.matrix = matrix.copy()
        self.dtype = dtype
        self.shape = matrix.shape
        self.queues = self.convert_to_queues()

    def convert_to_queues(self):
        return deque(deque(row) for row in self.matrix)

    def __iadd__(self, other):
        while other.queues:
            c = self.queues.popleft()
            c_other = other.queues.popleft()
            while c_other:
                d = c.popleft()
                d_other = c_other.popleft()
                c.append(d + d_other)

            self.queues.append(c)

        return self

    def convert_to_matrix(self):
        return [[item for item in row] for row in self.queues]

    def convert_to_cp_array(self):
        return cp.array(self.convert_to_matrix(), dtype=self.dtype)

    def __str__(self):
        return str(self.convert_to_matrix())


