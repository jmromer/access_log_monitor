from freezegun import freeze_time

from ..log_utils import now_utc
from .reporting_monitor import ReportingMonitor


@freeze_time("3:00:30pm")
def test_process_prints_summary_at_end_of_each_interval(mocker, capsys):
    fake_analyzer = mocker.Mock(**{"report.return_value": dict(hits=10)})
    monitor = ReportingMonitor(interval_sec=30)

    # 30 seconds later
    with freeze_time("3:01:00pm"):
        curr_time = now_utc()
        monitor.process(analyzer=fake_analyzer)
        out, _ = capsys.readouterr()
        assert f"Summary {curr_time}" in out
        assert "hits: 10" in out

    # 45 seconds later
    with freeze_time("3:01:15pm"):
        curr_time = now_utc()
        monitor.process(analyzer=fake_analyzer)
        out, _ = capsys.readouterr()
        assert out == ""

    # 60 seconds later
    with freeze_time("3:01:30pm"):
        curr_time = now_utc()
        monitor.process(analyzer=fake_analyzer)
        out, _ = capsys.readouterr()
        assert f"Summary {curr_time}" in out
        assert "hits: 10" in out
