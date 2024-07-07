from tests.field_ops.inplace.linked_list_inplace_tests import compare_inplace



inplace_ops = [
  "__iadd__",
  "__isub__",
  # Scalar
  # "__imul__",
  # "__itruediv__",
  # "__ifloordiv__",
  # "__imod__",
  # "__ipow__"
]

for op in inplace_ops:
  print("\n")
  compare_inplace(op)