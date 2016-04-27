from oem.core.match import EpisodeMatch
from tests.services.anidb.fixtures import client

import pytest


def test_show_invalid(client):
    assert client['anidb'].to('tvdb').map('INVALID', 1, 1) is None


def test_show_matches(client):
    assert client['anidb'].to('tvdb').map('1', 1, 1) == EpisodeMatch(1, 1)
    assert client['anidb'].to('tvdb').map('4', 1, 1) == EpisodeMatch(2, 1)


def test_season_matches(client):
    assert client['anidb'].to('tvdb').map('1041', 1,  1) == EpisodeMatch(1, 1)
    assert client['anidb'].to('tvdb').map('1041', 1, 41) == EpisodeMatch(7, 1)


def test_season_missing_number(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('202', None, None)


def test_episode_matches(client):
    assert client['anidb'].to('tvdb').map('202', 1, 1) == EpisodeMatch(0, 2)
    assert client['anidb'].to('tvdb').map('202', 1, 2) == EpisodeMatch(0, 2)


def test_episode_missing_number(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('202', 1, None)


def test_timeline_matches(client):
    assert client['anidb'].to('tvdb').map('1491', 1, 1, progress=3) == EpisodeMatch(1, 1)
    assert client['anidb'].to('tvdb').map('1491', 1, 1, progress=53) == EpisodeMatch(1, 2)


def test_timeline_missing_progress(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('1491', 1, 1)
