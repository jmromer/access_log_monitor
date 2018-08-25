from typing import List

from .log_analyzer import LogAnalyzer
from .log_manager import LogManager
from .log_monitors import LogMonitor
from .log_store import LogStore


def perform_monitoring(log: LogManager, datastore: LogStore,
                       analyzer: LogAnalyzer,
                       monitors: List[LogMonitor]) -> None:
    """
    Perform a single iteration of log monitoring.

    When the file has been updated, read the most recent entry and persist it
    to the datastore.

    At every iteration, perform monitoring tasks delegated to LogMonitor
    objects.
    """
    if log.has_been_updated:
        entry = log.last_entry
        datastore.add(entry)
    for monitor in monitors:
        monitor.process(analyzer)
