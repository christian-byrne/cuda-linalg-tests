
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

    def inplace_op(self, other, op):
        """NOTE: Adds speed overhead compared with defining inplace ops directly."""
        while other.queues:
            c = self.queues.popleft()
            c_other = other.queues.popleft()
            while c_other:
                d = c.popleft()
                d_other = c_other.popleft()
                c.append(d.__getattribute__(op)(d_other))

            self.queues.append(c)

    def __imul__(self, other):
        self.inplace_op(other, '__mul__')
        return self
    
    def __itruediv__(self, other):
        self.inplace_op(other, '__truediv__')
        return self
    
    def __ifloordiv__(self, other):
        self.inplace_op(other, '__floordiv__')
        return self
    
    def __imod__(self, other):
        self.inplace_op(other, '__mod__')
        return self
    
    def __ipow__(self, other):
        self.inplace_op(other, '__pow__')
        return self

    def __isub__(self, other):
        self.inplace_op(other, '__sub__')
        return self

    def __iadd__(self, other):
        self.inplace_op(other, '__add__')
        return self

    def convert_to_matrix(self):
        return [[item for item in row] for row in self.queues]

    def convert_to_cp_array(self):
        return cp.array(self.convert_to_matrix(), dtype=self.dtype)

    def __str__(self):
        return str(self.convert_to_matrix())


