from util.compare import compare, gr
from structures.linked_list_matrix import MatrixLinkedList


def compare_closed_inplace(op, mn=256, n=2):
    validate_works(op)

    matrices = gr(mn, n)
    lmatrices = [MatrixLinkedList(matrix) for matrix in matrices]

    def op_inplace_linkedlist_matrix(matrix1, matrix2):
        matrix1.__getattribute__(op)(matrix2)

    def op_inplace_matrix(matrix1, matrix2):
        matrix1.__getattribute__(op)(matrix2)

    return compare(
        (op_inplace_linkedlist_matrix, tuple(lmatrices), 1_000),
        (op_inplace_matrix, tuple(matrices), 1_000),
        title=f"{op} Inplace Comparison",
    ).p()


def validate_works(op):
    matrices = gr(4, 2)
    lmatrices = [MatrixLinkedList(matrix) for matrix in matrices]

    def assert_same_result():
        orig_1 = matrices[0].copy()
        orig_2 = matrices[1].copy()
        matrices[0].__getattribute__(op)(matrices[1])
        lmatrices[0].__getattribute__(op)(lmatrices[1])

        bool_m1 = matrices[0] == lmatrices[0].convert_to_cp_array()
        if not bool_m1.all():
            print(bool_m1)
            print("Matrix")
            print(matrices[0])
            print("LMatrix")
            print(lmatrices[0].convert_to_cp_array())
            print("original matrix 1")
            print(orig_1)
            print("original matrix 2")
            print(orig_2)
            raise ValueError("Not same result")

    assert_same_result()
    return True
