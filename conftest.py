import os

import pytest


@pytest.fixture
def project_root():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def sample_log_path(project_root):
    return os.path.join(project_root, "access_log_monitor", "test_fixtures",
                        "sample_log.log")
