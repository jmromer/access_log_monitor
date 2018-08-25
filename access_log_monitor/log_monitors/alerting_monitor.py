from datetime import timedelta
from inspect import cleandoc

from access_log_monitor.log_analyzer import LogAnalyzer
from access_log_monitor.log_utils import now_utc

from .log_monitor import LogMonitor


class AlertingMonitor(LogMonitor):
    """
    Continuously tracks the average requests per second over a rolling window
    of length (in seconds) `interval_sec`.

    When traffic exceeds a given threshold value `threshold_rps`, issues a
    high-traffic alert. If and when traffic falls back below the threshold
    level, issues a recovery alert.

    TODO: Extract printing
    """

    def __init__(self, threshold_rps: int, interval_sec: int) -> None:
        self.threshold_rps = threshold_rps
        self.interval_sec = interval_sec
        self.interval_delta = timedelta(seconds=interval_sec)
        self.in_alerted_state = False
        self.alert_start = None

    def process(self, analyzer: LogAnalyzer) -> None:
        curr_time = now_utc()
        interval_start = curr_time - self.interval_delta
        avg_reqs_per_sec = analyzer.requests_per_second(
            since=interval_start, current_time=curr_time)

        if avg_reqs_per_sec >= self.threshold_rps:
            self.__trigger_alert(curr_time, avg_reqs_per_sec)
        else:
            self.__recover_from_alert(curr_time)

    def __trigger_alert(self, curr_time, avg_reqs_per_sec):
        """
        Internal. No-ops unless not currently in alerted state.

        Enter alert state, compute the average requests received per second
        over the sampling interval, and print an alert mesage to stdout.
        """
        if self.in_alerted_state:
            return

        self.in_alerted_state = True
        self.alert_start = curr_time

        alert = f"""
        [ALERT] High traffic generated an alert - hits/sec: {avg_reqs_per_sec}, triggered at {curr_time}.
        """
        print(cleandoc(alert), "\n")

    def __recover_from_alert(self, curr_time):
        """
        Internal. No-ops unless currently in alerted state and we have an alert
        start time set.

        Recover from alert, compute the alert duration and print a recovery
        message to stdout.
        """
        if not self.in_alerted_state or not self.alert_start:
            return

        alert_duration = (curr_time - self.alert_start).total_seconds()
        self.in_alerted_state = False
        self.alert_start = None

        recover_message = f"""
        [ALERT] High traffic alert recovered at {curr_time}. Duration: {alert_duration}s.
        """
        print(cleandoc(recover_message), "\n")
