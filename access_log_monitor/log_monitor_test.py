import os

import pytest
from freezegun import freeze_time

from .log_analyzer import LogAnalyzer
from .log_manager import LogManager
from .log_monitor import perform_monitoring
from .log_monitors import AlertingMonitor
from .log_store import DequeDataStore


@pytest.mark.skip("TBD")
def test_interval_statistics():
    """
    Display stats every 10s about the traffic during those 10s: the sections of
    the web site with the most hits, as well as interesting summary statistics
    on the traffic as a whole.
    """


@freeze_time("2018-09-11 3:30:00", tz_offset=0)
def test_high_traffic_alerting(capsys, project_root):
    """
    Whenever total traffic for the past 2 minutes exceeds a certain number on
    average, add a message saying that
    "High traffic generated an alert - hits = {value}, triggered at {time}".

    The default threshold should be 10 requests per second and should be
    overridable.
    """
    # 1 minute of log entries coming in at 1 request per second
    entries_file = os.path.join(project_root, "access_log_monitor",
                                "test_fixtures", "logged_1rps.log")

    # create temp log file
    temp_file = os.path.join(project_root, "data", "test_alerting.log")
    open(temp_file, "w+").close()

    # initialize log manager, datastore, analysis manager
    log_mgr = LogManager(path=temp_file)
    in_memory_datastore = DequeDataStore()
    analysis_manager = LogAnalyzer(in_memory_datastore)

    # alert when hits exceed 1 req per second on average over 1 minute
    alerting = AlertingMonitor(threshold_rps=1, interval_sec=60)

    with open(entries_file, "r") as entries_f:
        for line in entries_f.readlines():
            with open(temp_file, "a") as templog:
                templog.write(line)

            # each time the log is updated, perform monitoring
            perform_monitoring(
                log=log_mgr,
                datastore=in_memory_datastore,
                analyzer=analysis_manager,
                monitors=[alerting])

    # 61 log entries
    assert len(in_memory_datastore.datastore) == 61

    # alert is triggered
    out, _ = capsys.readouterr()
    assert "[ALERT] High traffic generated an alert" in out
    assert "hits/sec: 1.0" in out

    # teardown temp file
    os.remove(temp_file)


@freeze_time("2018-09-11 3:30:00", tz_offset=0)
def test_return_to_normal_traffic_alerting(capsys, project_root):
    """
    Whenever the total traffic drops again below that value on average for the
    past 2 minutes, print or displays another message detailing when the alert
    recovered.
    """
    # 1 minute of log entries coming in at 1 request per second
    entries_file = os.path.join(project_root, "access_log_monitor",
                                "test_fixtures", "logged_1rps.log")

    # create temp log file
    temp_file = os.path.join(project_root, "data", "test_alerting.log")
    open(temp_file, "w+").close()

    # initialize log manager, datastore, analysis manager
    log_mgr = LogManager(path=temp_file)
    in_memory_datastore = DequeDataStore()
    analysis_manager = LogAnalyzer(in_memory_datastore)

    # alert when hits exceed 1 req per second on average over 1 minute
    alerting = AlertingMonitor(threshold_rps=1, interval_sec=60)

    with open(entries_file, "r") as entries_f:
        for line in entries_f.readlines():
            with open(temp_file, "a") as templog:
                templog.write(line)

            # each time the log is updated, perform monitoring
            perform_monitoring(
                log=log_mgr,
                datastore=in_memory_datastore,
                analyzer=analysis_manager,
                monitors=[alerting])

    # 61 log entries
    assert len(in_memory_datastore.datastore) == 61

    # alert is triggered
    out, _ = capsys.readouterr()
    assert "[ALERT] High traffic generated an alert" in out
    assert "hits/sec: 1.0" in out

    # Perform monitoring again after a minute has passed
    with freeze_time("2018-09-11 3:31:00", tz_offset=0, tick=True):
        perform_monitoring(
            log=log_mgr,
            datastore=in_memory_datastore,
            analyzer=analysis_manager,
            monitors=[alerting])

    out, _ = capsys.readouterr()
    assert "[ALERT] High traffic alert recovered" in out
    assert "Duration: 60.0s" in out

    # teardown temp file
    os.remove(temp_file)
