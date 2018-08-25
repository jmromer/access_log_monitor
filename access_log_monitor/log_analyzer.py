from datetime import datetime
from typing import Any, Dict, Optional

from .log_store import DequeDataStore, LogStore
from .log_utils import most_common_by, now_utc, percent


class LogAnalyzer:
    def __init__(self, datastore: Optional[LogStore] = None) -> None:
        self.store: LogStore = datastore or DequeDataStore()

    def requests_per_second(self,
                            since: datetime,
                            current_time: Optional[datetime] = None) -> float:
        """
        Query the datastore for entries since the given time `since` and
        compute the average number of requests per second over that interval.
        """
        current_time = current_time or now_utc()
        hits_over_interval = len(self.store.peek(since))
        seconds_in_interval = (current_time - since).total_seconds()

        if not seconds_in_interval:
            return 0.0

        return round(hits_over_interval / seconds_in_interval, 1)

    def report(self, since: datetime) -> Dict[str, Any]:
        """
        Generate summary statistics for all traffic logged since the given time
        `since`.

        Entries:

        - Most popular site section (section name)
        - Most popular site section (count of visits)
        - Total requests processed since the cutoff time
        - Average requests per second since the cutoff time
        - Percentage of requests with 2xx responses
        - Percentage of requests with 3xx responses
        - Percentage of requests with 4xx responses
        - Percentage of requests with 5xx responses

        Return a dict.
        """
        entries = self.store.peek(since)
        most_common = most_common_by(lambda e: e.site_section, entries)

        return {
            "most_popular_section": most_common["value"],
            "most_popular_count": most_common["count"],
            "requests_processed": len(entries),
            "requests_per_second": self.requests_per_second(since),
            "response_2xx_pct": percent(lambda e: e.status[0] == "2", entries),
            "response_3xx_pct": percent(lambda e: e.status[0] == "3", entries),
            "response_4xx_pct": percent(lambda e: e.status[0] == "4", entries),
            "response_5xx_pct": percent(lambda e: e.status[0] == "5", entries),
        }
