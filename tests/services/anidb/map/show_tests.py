from oem.media.movie import MovieIdentifier
from oem.media.show import EpisodeIdentifier, EpisodeMatch

from tests.services.anidb.fixtures import client
import pytest


#
# Matches
#


def test_matches_anidb_episode(client):
    assert client['tvdb'].to('anidb').map('72025', EpisodeIdentifier(4, 12)) == EpisodeMatch({'anidb': '2673'}, 1, 12)
    assert client['tvdb'].to('anidb').map('72025', EpisodeIdentifier(5, 25)) is None

    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(15, 20)) == EpisodeMatch({'anidb': '9216'}, 1, 20)
    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(15, 39)) == EpisodeMatch({'anidb': '9764'}, 1, 1)
    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(15, 40)) == EpisodeMatch({'anidb': '9764'}, 1, 2)


def test_matches_anidb_episode_absolute(client):
    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(1,  1,   1)) == EpisodeMatch({'anidb': '230'}, absolute_num=1)
    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(1, 82,  82)) == EpisodeMatch({'anidb': '230'}, absolute_num=82)
    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(3,  4, 122)) == EpisodeMatch({'anidb': '230'}, absolute_num=122)


def test_matches_tvdb_episode(client):
    assert client['anidb'].to('tvdb').map('1', EpisodeIdentifier(1, 1)) == EpisodeMatch({'tvdb': '72025'}, 1, 1)

    assert client['anidb'].to('tvdb').map('4', EpisodeIdentifier(1, 1)) == EpisodeMatch({'tvdb': '72025'}, 2, 1)

    assert client['anidb'].to('tvdb').map('202', EpisodeIdentifier(1, 1)) == EpisodeMatch({'tvdb': '70350'}, 0, 2)
    assert client['anidb'].to('tvdb').map('202', EpisodeIdentifier(1, 2)) == EpisodeMatch({'tvdb': '70350'}, 0, 2)

    assert client['anidb'].to('tvdb').map('1041', EpisodeIdentifier(1,  1)) == EpisodeMatch({'tvdb': '76703'}, 1, 1)
    assert client['anidb'].to('tvdb').map('1041', EpisodeIdentifier(1, 41)) == EpisodeMatch({'tvdb': '76703'}, 7, 1)

    assert client['anidb'].to('tvdb').map('1045', EpisodeIdentifier(1, 1)) == EpisodeMatch({'tvdb': '81472'}, 0, 5)

    assert client['anidb'].to('tvdb').map('5101', EpisodeIdentifier(0, 2)) == EpisodeMatch({'tvdb': '80644'}, 0, 2)
    assert client['anidb'].to('tvdb').map('5101', EpisodeIdentifier(1, 2)) == EpisodeMatch({'tvdb': '80644'}, 1, 2)
    assert client['anidb'].to('tvdb').map('5101', EpisodeIdentifier(2, 2)) == EpisodeMatch({'tvdb': '80644'}, 2, 2)


def test_matches_tvdb_episode_absolute(client):
    assert client['anidb'].to('tvdb').map('230', EpisodeIdentifier(2, 52, 52)) == EpisodeMatch({'tvdb': '76703'}, absolute_num=52)


def test_matches_tvdb_episode_timeline(client):
    assert client['anidb'].to('tvdb').map('1491', EpisodeIdentifier(1, 1, progress=3)) == EpisodeMatch({'tvdb': '232511'}, 1, 1)
    assert client['anidb'].to('tvdb').map('1491', EpisodeIdentifier(1, 1, progress=53)) == EpisodeMatch({'tvdb': '232511'}, 1, 2)


#
# Invalid / Missing
#


def test_invalid_identifier(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('202', EpisodeIdentifier(None, None))

    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('202', EpisodeIdentifier(1, None))

    with pytest.raises(ValueError):
        assert client['anidb'].to('tvdb').map('1045', MovieIdentifier())

    with pytest.raises(ValueError):
        assert client['anidb'].to('tvdb').map('1045')


def test_invalid_timeline(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('1491', EpisodeIdentifier(1, 1))


def test_missing_item(client):
    assert client['anidb'].to('tvdb').map('missing', EpisodeIdentifier(1, 1)) is None


def test_missing_default_season(client):
    assert client['anidb'].to('tvdb').map('no_default_season', EpisodeIdentifier(1, 1)) is None
