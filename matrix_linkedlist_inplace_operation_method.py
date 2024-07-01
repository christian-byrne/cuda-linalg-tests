import cupy as cp
from collections import deque
from util.compare import compare, gr


class MatrixLinkedList:
    def __init__(self, matrix):
        self.matrix = matrix.copy()
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
        # 1. Efficient List Construction
        data = [[item for item in row] for row in self.queues]

        # 2. Direct CuPy Array Creation
        cp_array = cp.array(data)  # Adjust dtype if needed
        return cp_array

    def __str__(self):
        return str(self.convert_to_matrix())


matrices = gr(256, 2)
lmatrices = [MatrixLinkedList(matrix.copy()) for matrix in matrices]

def add_inplace_linkedlist_matrix(matrix1, matrix2):
    matrix1 += matrix2

def add_inplace_matrix(matrix1, matrix2):
    matrix1 += matrix2

compare(
    (add_inplace_linkedlist_matrix, tuple(lmatrices), 50),
    (add_inplace_matrix, tuple(matrices), 50),
).p()

matrices = gr(4, 2)
lmatrices = [MatrixLinkedList(matrix) for matrix in matrices]


def assert_same_result():
    orig_1 = matrices[0].copy()
    orig_2 = matrices[1].copy()
    matrices[0] += matrices[1]
    lmatrices[0] += lmatrices[1]

    bool_m1 = matrices[0] == lmatrices[0].convert_to_cp_array()
    if bool_m1.all():
        print("Results are the same")
    else:
        print(bool_m1)
        print("Matrix")
        print(matrices[0])
        print("LMatrix")
        print(lmatrices[0].convert_to_cp_array())
        print("original matrix 1")
        print(orig_1)
        print("original matrix 2")
        print(orig_2)

assert_same_result()
