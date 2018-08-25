import os
from random import randint
from time import sleep

import pytest

from .log_line import LogLine
from .log_manager import LogManager


def test_constructor_raises_if_file_doesnt_exist():
    with pytest.raises(FileNotFoundError) as err:
        LogManager(f"./notfound-{randint(1, 100)}.log")
    assert "No such file or directory" in str(err.value)


def test_last_entry(sample_log_path):
    log = LogManager(sample_log_path)
    last_entry = log.last_entry

    assert isinstance(last_entry, LogLine)
    assert last_entry.ip_address == "127.0.0.1"
    assert last_entry.timestamp == "11/Sep/2018 03:29:55 +0000"
    assert last_entry.verb == "GET"
    assert last_entry.version == "1.0"
    assert last_entry.path == "/pages/delete"
    assert last_entry.status == "500"


def test_last_updated_at_returns_rounded_unix_epoch_time(sample_log_path):
    log = LogManager(sample_log_path)
    last_updated_epoch_time = log.last_updated_at
    assert isinstance(last_updated_epoch_time, float)
    assert last_updated_epoch_time > 0


def test_has_been_updated_returns_true_if_theres_been_update():
    # create temp log, write to file
    temp_file_path = "test_has_been_updated.log"
    with open(temp_file_path, "w+") as templog:
        templog.write("line 1\n")

    # create log manager
    log = LogManager(temp_file_path)
    first_update_time = log.mru_time
    assert log.has_been_updated is False

    # tick tock
    sleep(0.001)

    # update the file
    with open(temp_file_path, "w") as templog:
        templog.write("line 2\n")

    # has_been_updated returns true if updated
    assert log.last_updated_at > first_update_time
    assert log.has_been_updated is True

    # remove temp file
    os.remove(temp_file_path)


def test_has_been_updated_returns_false_if_log_hasnt_been_updated():
    # create temp log, write to file
    temp_file_path = "test_has_been_updated.log"
    with open(temp_file_path, "w+") as templog:
        templog.write("line 1\n")

    # create log manager
    log = LogManager(temp_file_path)
    first_update_time = log.mru_time
    assert log.has_been_updated is False

    # has_been_updated returns false if not updated
    assert log.last_updated_at == first_update_time
    assert log.has_been_updated is False

    # remove temp file
    os.remove(temp_file_path)
