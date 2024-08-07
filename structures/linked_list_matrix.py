from collections import deque
import cupy as cp

# import cProfile
from functools import lru_cache


class MatrixLinkedList:
    def __init__(self, matrix, dtype=None):
        self.matrix = matrix.copy()
        self.dtype = dtype
        self.shape = matrix.shape
        self.queues = self.convert_to_queues()

    def convert_to_queues(self):
        return deque(deque(row) for row in self.matrix)

    @lru_cache(maxsize=32)
    def create_scalar_linkedlist_matrix(self, scalar):
        """For scalar operations, create a linked list matrix from the scalar and cache it."""
        scalar_cupy = cp.array(scalar)
        like_matrix = cp.full_like(self.matrix, scalar_cupy)
        return MatrixLinkedList(like_matrix)

    def inplace_op_scalar(self, scalar, op):
        scalar_matrix = self.create_scalar_linkedlist_matrix(scalar)
        self.inplace_op_closed(scalar_matrix, op)

    def inplace_op_closed(self, other, op):
        """NOTE: Adds speed overhead compared with defining inplace ops directly."""
        while other.queues:
            c = self.queues.popleft()
            c_other = other.queues.popleft()
            while c_other:
                d = c.popleft()
                d_other = c_other.popleft()
                c.append(d.__getattribute__(op)(d_other))

            self.queues.append(c)

    def __iadd__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__add__")
        else:
            self.inplace_op_closed(other, "__add__")
        return self

    def __imul__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__mul__")
        else:
            self.inplace_op_closed(other, "__mul__")
        return self

    def __itruediv__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__truediv__")
        else:
            self.inplace_op_closed(other, "__truediv__")
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__floordiv__")
        else:
            self.inplace_op_closed(other, "__floordiv__")

        return self

    def __imod__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__mod__")
        else:
            self.inplace_op_closed(other, "__mod__")
        return self

    def __ipow__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__pow__")
        else:
            self.inplace_op_closed(other, "__pow__")
        return self

    def __isub__(self, other):
        if isinstance(other, (int, float, complex)):
            self.inplace_op_scalar(other, "__sub__")
        else:
            self.inplace_op_closed(other, "__sub__")
        return self

    def convert_to_matrix(self):
        return [[item for item in row] for row in self.queues]

    def convert_to_cp_array(self):
        return cp.array(self.convert_to_matrix(), dtype=self.dtype)

    def __str__(self):
        return str(self.convert_to_matrix())
