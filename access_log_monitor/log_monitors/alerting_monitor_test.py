from freezegun import freeze_time

from ..log_utils import now_utc
from .alerting_monitor import AlertingMonitor


def test_process_alerts_if_unalerted_and_over_threshold_rps(mocker, capsys):
    fake_analyzer = mocker.Mock(**{"requests_per_second.return_value": 1.5})
    monitor = AlertingMonitor(threshold_rps=1, interval_sec=30)

    monitor.process(analyzer=fake_analyzer)

    out, _ = capsys.readouterr()
    assert "[ALERT] High traffic generated an alert" in out
    assert "hits/sec: 1.5" in out


def test_process_no_ops_if_unalerted_and_below_threshold_rps(mocker, capsys):
    fake_analyzer = mocker.Mock(**{"requests_per_second.return_value": 0.5})
    monitor = AlertingMonitor(threshold_rps=1, interval_sec=30)

    monitor.process(analyzer=fake_analyzer)

    out, _ = capsys.readouterr()
    assert out == ""


@freeze_time("3:30pm")
def test_process_recovers_if_alerted_and_below_threshold_rps(mocker, capsys):
    fake_analyzer = mocker.Mock(**{"requests_per_second.return_value": 0.5})
    monitor = AlertingMonitor(threshold_rps=1, interval_sec=30)
    monitor.in_alerted_state = True
    monitor.alert_start = now_utc(minute=29)

    monitor.process(analyzer=fake_analyzer)

    out, _ = capsys.readouterr()
    assert f"[ALERT] High traffic alert recovered" in out
    assert "Duration: 60.0s" in out


def test_process_no_ops_if_alerted_and_above_threshold_rps(mocker, capsys):
    fake_analyzer = mocker.Mock(**{"requests_per_second.return_value": 1.5})
    monitor = AlertingMonitor(threshold_rps=1, interval_sec=30)
    monitor.in_alerted_state = True

    monitor.process(analyzer=fake_analyzer)

    out, _ = capsys.readouterr()
    assert out == ""
