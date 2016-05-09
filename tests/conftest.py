from oem.media.show.match import EpisodeMatch


def pytest_assertrepr_compare(op, left, right):
    if op == "==" and isinstance(left, EpisodeMatch) and isinstance(right, EpisodeMatch):
        return [
            '%r == %r' % (left, right)
        ]
