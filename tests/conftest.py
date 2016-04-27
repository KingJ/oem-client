from oem.core.match import EpisodeMatch


def pytest_assertrepr_compare(op, left, right):
    if op == "==" and isinstance(left, EpisodeMatch) and isinstance(right, EpisodeMatch):
        return [
            'EpisodeMatch(%r, %r) != EpisodeMatch(%r, %r)' % (
                left.season, left.number,
                right.season, right.number
            )
        ]
