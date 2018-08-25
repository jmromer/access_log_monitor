import abc

from access_log_monitor.log_analyzer import LogAnalyzer


class LogMonitor(metaclass=abc.ABCMeta):
    """
    Abstract base class for LogMonitor classes.
    """

    @abc.abstractmethod
    def process(self, analyzer: LogAnalyzer) -> None:
        """
        Defines the logic to be performed by the monitor each time the target
        log is checked.
        """
