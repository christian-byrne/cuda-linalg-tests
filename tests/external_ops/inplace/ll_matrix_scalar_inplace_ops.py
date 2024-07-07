from util.compare import compare, gr
from structures.linked_list_matrix import MatrixLinkedList
import random


def compare_external_inplace(op, mn=256, scalar_range=10):
    validate_works(op)

    matrix = gr(mn, 1)
    lmatrix = MatrixLinkedList(matrix)
    scalar = int(random.random() * scalar_range)

    def op_inplace_external_linkedlist_matrix(matrix1, scalar):
        matrix1.__getattribute__(op)(scalar)

    def op_inplace_external_matrix(matrix1, scalar):
        matrix1.__getattribute__(op)(scalar)

    return compare(
        (op_inplace_external_linkedlist_matrix, tuple([lmatrix, scalar]), 500),
        (op_inplace_external_matrix, tuple([matrix, scalar]), 500),
        title=f"{op} (Scalar) Inplace Comparison",
    ).p()


def validate_works(op):
    matrix = gr(4, 1)
    lmatrix = MatrixLinkedList(matrix)
    scalar = int(random.random() * 10)

    def assert_same_result():
        orig_1 = matrix.copy()
        orig_scalar = scalar

        matrix.__getattribute__(op)(scalar)
        lmatrix.__getattribute__(op)(scalar)

        bool_termequality_matrix_ = matrix == lmatrix.convert_to_cp_array()
        if not bool_termequality_matrix_.all():
            print(bool_termequality_matrix_)
            print("Matrix")
            print(matrix)
            print("LMatrix")
            print(lmatrix.convert_to_cp_array())
            print("original Matrix")
            print(orig_1)
            print("original scalar")
            print(orig_scalar)
            raise ValueError("Not same result")

    assert_same_result()
    return True
