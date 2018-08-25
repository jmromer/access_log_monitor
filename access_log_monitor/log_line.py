from typing import Pattern

from dataclasses import dataclass

from .log_entry_format import PATH_FORMAT, TIMESTAMP_FORMAT, W3C_ENTRY_FORMAT


@dataclass
class LogLine:
    ip_address: str = ""
    username: str = ""
    timestamp: str = ""
    verb: str = ""
    path: str = ""
    version: str = ""
    status: str = ""
    size: str = ""
    timestamp_format: str = TIMESTAMP_FORMAT
    entry_format: Pattern = W3C_ENTRY_FORMAT

    @property
    def site_section(self) -> str:
        """The section of the site indicated by the log entry's `path`."""
        match = PATH_FORMAT.match(self.path)
        if match:
            return match.group("base_path")
        return ""

    @classmethod
    def from_log_line(cls, log_line: str):
        """
        Parse the given log line into a LogLine model instance.
        If parsing is successful, return a LogLine. Else return None.
        """
        match = cls.entry_format.match(log_line)
        if not match:
            return None

        date = match.group("date")
        time = match.group("time")
        offset = match.group("offset")

        entry = cls(
            ip_address=match.group("ip_address"),
            username=match.group("username"),
            timestamp=f"{date} {time} {offset}",
            verb=match.group("verb"),
            path=match.group("path"),
            version=match.group("http_version"),
            status=match.group("response_status"),
            size=match.group("size"))

        return entry
