from oem.media.movie import MovieIdentifier, MovieMatch
from oem.media.show import EpisodeIdentifier

from tests.services.anidb.fixtures import client
import pytest


#
# Matches
#


def test_matches_imdb_episode(client):
    assert client['anidb'].to('imdb').map('1045', EpisodeIdentifier(1, 1)) == MovieMatch({'imdb': 'tt1125254'})


def test_matches_imdb_movie(client):
    assert client['anidb'].to('imdb').map('1043', MovieIdentifier()) == MovieMatch({'imdb': 'tt0142235'})
    assert client['anidb'].to('imdb').map('1045') == MovieMatch({'imdb': 'tt1125254'})


#
# Invalid / Missing
#


def test_invalid_identifier(client):
    assert client['anidb'].to('imdb').map('1045', EpisodeIdentifier(1, 2)) is None
