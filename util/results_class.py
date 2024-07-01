from cupyx.profiler._time import _PerfCaseResult
from typing import List
from rich.table import Table
from rich.console import Console


class Results:
    def __init__(self, results: List[_PerfCaseResult] = None):
        if results:
            self.res: List[_PerfCaseResult] = results
        else:
            self.res = []

        self.console = Console()

    @staticmethod
    def _to_str_per_item(device_name, t, table: Table, name: str = "Method Name"):
        assert t.ndim == 1
        assert t.size > 0
        t_us = t * 1e6
        mean_ = f"{t_us.mean():9.03f} us"
        if t.size > 1:
            er = f"{t_us.std():6.03f}"
            min_ = f"{t_us.min():9.03f}"
            max_ = f"{t_us.max():9.03f}"
            table.add_row(name, device_name, mean_, er, min_, max_)
        else:
            er = min_ = max_ = ""
            table.add_row(name, device_name, mean_)

    @staticmethod
    def create_table(title: str = "Results"):
        table = Table(title=title)
        table.add_column("Method Name", justify="center", style="cyan")
        table.add_column("Device", justify="center", style="cyan")
        table.add_column("Mean Time", justify="center", style="cyan")
        table.add_column("+/-", justify="center", style="green")
        table.add_column("Min", justify="center", style="red")
        table.add_column("Max", justify="center", style="blue")
        return table

    def append(self, res: str):
        self.res.append(res)
        return self

    def to_str(self) -> Table:
        tb = self.create_table()
        for result in self.res:
            self._to_str_per_item("CPU", result._ts[0], tb, result.name)
            for i, d in enumerate(result._devices):
                self._to_str_per_item(
                    "GPU-{}".format(d), result._ts[1 + i], tb, result.name
                )

        return tb

    def p(self):
        self.console.print(self.to_str())
        return self

    def __str__(self):
        return self.to_str()
