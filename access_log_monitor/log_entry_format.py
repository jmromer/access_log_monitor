import re

W3C_ENTRY_FORMAT = re.compile(r"""
(?P<ip_address>.+)          # source ip address
\s-\s
(?P<username>\w+)           # requesting user
\s\[
(?P<date>.+):               # timestamp date
(?P<time>\d{2}:\d{2}:\d{2}) # timestamp time
\s(?P<offset>[-+]\d{4})     # timestamp utc offset
\]\s"
(?P<verb>.+)                # http verb
\s
(?P<path>.+)                # endpoint path
\s
HTTP/(?P<http_version>.+)   # protocol version
"\s
(?P<response_status>\d+)    # response status code
\s
(?P<size>\d+)               # response payload size
""", re.VERBOSE)

TIMESTAMP_FORMAT = "%d/%b/%Y %H:%M:%S %z"

PATH_FORMAT = re.compile(r"^/(?P<base_path>\w+)/?.*$")
