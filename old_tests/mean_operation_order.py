from util.compare import compare, gr


scalar = 1 / 3


def mean_3_operations(A, B, C):
    return (A + B + C) * scalar


def mean_5_operations(A, B, C):
    return A * scalar + B * scalar + C * scalar


ms = gr(512, 3)
compare(
    (mean_5_operations, tuple(ms), 1_000),
    (mean_3_operations, tuple(ms), 1_000),
).p()

# RESULT: (A + B + C) * scalar is faster than A * scalar + B * scalar + C * scalar, as expected.