from .log_line import LogLine


def test_site_section_parses_base_path():
    entry = LogLine(path="/dashboard/name")
    assert entry.site_section == "dashboard"

    entry = LogLine(path="/account/subdir/")
    assert entry.site_section == "account"

    entry = LogLine(path="/home?version=1")
    assert entry.site_section == "home"


def test_site_section_returns_empty_string_if_parse_fails():
    entry = LogLine(path="whatever")
    assert entry.site_section == ""

    entry = LogLine(path="---")
    assert entry.site_section == ""

    entry = LogLine(path="https://google.com/mail")
    assert entry.site_section == ""
