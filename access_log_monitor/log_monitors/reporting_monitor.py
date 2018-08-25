from datetime import timedelta
from inspect import cleandoc

from access_log_monitor.log_analyzer import LogAnalyzer
from access_log_monitor.log_utils import is_interval_complete, now_utc

from .log_monitor import LogMonitor


class ReportingMonitor(LogMonitor):
    """
    Reports summary statistics at set intervals of length (in seconds)
    `interval_sec` on recent site traffic derived from the target log.

    TODO: Extract printing
    """

    def __init__(self, interval_sec: int) -> None:
        self.interval_sec = interval_sec
        self.interval_delta = timedelta(seconds=interval_sec)
        self.interval_start = now_utc()

    def process(self, analyzer: LogAnalyzer) -> None:
        curr_time = now_utc()
        is_interval_done = is_interval_complete(
            start_time=self.interval_start,
            delta=self.interval_delta,
            current_time=curr_time)

        if is_interval_done:
            stats = analyzer.report(since=self.interval_start)
            self.interval_start = curr_time

            entries = (": ".join(map(str, tup)) for tup in stats.items())
            summary = f"""
            Traffic Summary {curr_time}
            ---------------------------
            """
            print(cleandoc(summary))
            print("\n".join(entries), "\n")
