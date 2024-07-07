from tests.field_ops.inplace.ll_matrix_field_inplace_ops import (
    compare_closed_inplace,
)
from tests.external_ops.inplace.ll_matrix_scalar_inplace_ops import (
    compare_external_inplace,
)


inplace_closed_ops = [
    "__iadd__",
    "__isub__",
    # TODO
    # "__imul__",
    # "__ipow__"
]

# Scalar for Matrix
inplace_external_ops = [
    "__imul__",
    "__iadd__",
    "__isub__",
    "__ifloordiv__",
    "__imod__",
    "__ipow__",
]

for op in inplace_closed_ops:
    print("\n")
    compare_closed_inplace(op)

for op in inplace_external_ops:
    print("\n")
    compare_external_inplace(op)
