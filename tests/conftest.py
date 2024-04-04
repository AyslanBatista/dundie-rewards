MARKER = """\
integration: Mark integration tests
unit: Mark unit tests
high: High Priority
medium: Medium Priority
low: low Priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)
