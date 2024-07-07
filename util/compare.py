import cupy as cp
from cupyx.profiler import time_range, benchmark
from typing import Any, Tuple, Callable

from util.results_class import Results

Args = Tuple[Any, ...]
FuncInstructions = Tuple[Callable[..., Any], Args, int]


def gr(n=512, ct=1):
    return (
        cp.random.rand(n, n) if ct == 1 else [cp.random.rand(n, n) for _ in range(ct)]
    )


def compare(*fns: FuncInstructions, title: str = "Results"):
    results = Results(
        title=f"{title} (n={fns[0][2]}) (size={fns[1][1][0].shape[0]}x{fns[1][1][0].shape[1]})"
    )
    for fn, args, n_repeat in fns:
        with time_range(fn.__name__):
            results.append(benchmark(fn, args, n_repeat=n_repeat))
    return results
