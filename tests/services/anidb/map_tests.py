from oem.media.movie import MovieIdentifier, MovieMatch
from oem.media.show import EpisodeIdentifier, EpisodeMatch
from tests.services.anidb.fixtures import client

import pytest


#
# Movie Mapping
#

def test_movie_invalid(client):
    assert client['anidb'].to('imdb').map('1045', EpisodeIdentifier(1, 2)) is None


def test_movie_matches(client):
    assert client['anidb'].to('imdb').map('1043', MovieIdentifier()) == MovieMatch(
        {'imdb': 'tt0142235'}
    )

    assert client['anidb'].to('imdb').map('1045', EpisodeIdentifier(1, 1)) == MovieMatch(
        {'imdb': 'tt1125254'}
    )

    assert client['anidb'].to('imdb').map('1045') == MovieMatch(
        {'imdb': 'tt1125254'}
    )

#
# Show Mapping
#


def test_show_invalid(client):
    assert client['anidb'].to('tvdb').map('INVALID', EpisodeIdentifier(1, 1)) is None

    with pytest.raises(ValueError):
        assert client['anidb'].to('tvdb').map('1045', MovieIdentifier())

    with pytest.raises(ValueError):
        assert client['anidb'].to('tvdb').map('1045')


def test_show_matches(client):
    assert client['anidb'].to('tvdb').map('1', EpisodeIdentifier(1, 1)) == EpisodeMatch(
        {'tvdb': '72025'}, 1, 1
    )

    assert client['anidb'].to('tvdb').map('4', EpisodeIdentifier(1, 1)) == EpisodeMatch(
        {'tvdb': '72025'}, 2, 1
    )

    assert client['anidb'].to('tvdb').map('1045', EpisodeIdentifier(1, 1)) == EpisodeMatch(
        {'tvdb': '81472'}, 0, 5
    )

    assert client['anidb'].to('tvdb').map('5101', EpisodeIdentifier(0, 2)) == EpisodeMatch(
        {'tvdb': '80644'}, 0, 2
    )

    assert client['anidb'].to('tvdb').map('5101', EpisodeIdentifier(1, 2)) == EpisodeMatch(
        {'tvdb': '80644'}, 1, 2
    )

    assert client['anidb'].to('tvdb').map('5101', EpisodeIdentifier(2, 2)) == EpisodeMatch(
        {'tvdb': '80644'}, 2, 2
    )


#
# Season Mapping
#


def test_season_invalid(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('202', EpisodeIdentifier(None, None))


def test_season_matches(client):
    assert client['anidb'].to('tvdb').map('1041', EpisodeIdentifier(1,  1)) == EpisodeMatch(
        {'tvdb': '76703'}, 1, 1
    )

    assert client['anidb'].to('tvdb').map('1041', EpisodeIdentifier(1, 41)) == EpisodeMatch(
        {'tvdb': '76703'}, 7, 1
    )

    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(15, 20)) == EpisodeMatch(
        {'anidb': '9216'}, 1, 20
    )


#
# Episode Mapping
#


def test_episode_invalid(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('202', EpisodeIdentifier(1, None))


def test_episode_matches(client):
    assert client['anidb'].to('tvdb').map('202', EpisodeIdentifier(1, 1)) == EpisodeMatch(
        {'tvdb': '70350'}, 0, 2
    )

    assert client['anidb'].to('tvdb').map('202', EpisodeIdentifier(1, 2)) == EpisodeMatch(
        {'tvdb': '70350'}, 0, 2
    )

    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(15, 39)) == EpisodeMatch(
        {'anidb': '9764'}, 1, 1
    )

    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(15, 40)) == EpisodeMatch(
        {'anidb': '9764'}, 1, 2
    )


def test_episode_matches_absolute(client):
    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(1,  1,   1)) == EpisodeMatch(
        {'anidb': '230'},
        absolute_num=1
    )

    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(1, 82,  82)) == EpisodeMatch(
        {'anidb': '230'},
        absolute_num=82
    )

    assert client['tvdb'].to('anidb').map('76703', EpisodeIdentifier(3,  4, 122)) == EpisodeMatch(
        {'anidb': '230'},
        absolute_num=122
    )


def test_episode_timeline_invalid(client):
    with pytest.raises(ValueError):
        client['anidb'].to('tvdb').map('1491', EpisodeIdentifier(1, 1))


def test_episode_timeline_matches(client):
    assert client['anidb'].to('tvdb').map('1491', EpisodeIdentifier(1, 1, progress=3)) == EpisodeMatch(
        {'tvdb': '232511'}, 1, 1
    )

    assert client['anidb'].to('tvdb').map('1491', EpisodeIdentifier(1, 1, progress=53)) == EpisodeMatch(
        {'tvdb': '232511'}, 1, 2
    )
