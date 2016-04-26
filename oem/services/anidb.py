from oem.core.match import EpisodeMatch
from oem.services.core.base import Service

import logging

log = logging.getLogger(__name__)


class AniDbService(Service):
    __services__ = {
        'anidb':    ['imdb', 'tvdb'],
        'imdb':     ['anidb'],
        'tvdb':     ['anidb']
    }

    def __init__(self, client, source, target):
        super(AniDbService, self).__init__(client, source, target)

        self.loaded = False

    def load(self):
        if self.loaded:
            raise Exception('Service already loaded')

        # Try find installed database package
        database_path = self.find_database()

        if not database_path:
            # TODO Download database index
            raise NotImplementedError

        log.info('Using database: %r', database_path)

        # Load collection
        self.load_collection()

        # Finished loading service
        log.info('Loaded service: %-5s -> %-5s', self.source, self.target)
        self.loaded = True

    def get(self, key, default=None):
        # Retrieve item metadata
        metadata = self.get_metadata(key)

        if metadata is None:
            return default

        # TODO check for updates

        # Retrieve item from disk
        return metadata.get()

    def get_metadata(self, key, default=None):
        try:
            return self.collection[key]
        except KeyError:
            return default

    def map(self, key, season_num=None, episode_num=None, progress=None):
        # Retrieve item
        item = self.get(key)

        if item is None:
            return None

        try:
            default_season = int(item.parameters['default_season'])
        except Exception:
            default_season = None

        # Default Season
        if not item.seasons:
            if default_season is None:
                return None

            episode_offset = int(item.parameters.get('episode_offset', 0))

            return EpisodeMatch(default_season, episode_num + episode_offset)

        # Find season
        if season_num is None:
            raise ValueError('Missing required parameter "season_num"')

        season = item.seasons.get(str(season_num))

        if not season:
            if default_season is not None:
                return EpisodeMatch(default_season, episode_num)

            return None

        # Season Mapping
        if not season.episodes:
            if episode_num is None:
                raise ValueError('Missing required parameter "episode_num"')

            for season_mapping in season.mappings:
                if not (season_mapping.start <= episode_num <= season_mapping.end):
                    continue

                pass

            raise NotImplementedError

        # Find episode
        if episode_num is None:
            raise ValueError('Missing required parameter "episode_num"')

        episode = season.episodes.get(str(episode_num))

        if not episode:
            return None

        # Episode Mapping
        for episode_mapping in episode.mappings:
            if episode_mapping.timeline and 'source' in episode_mapping.timeline:
                if progress is None:
                    raise ValueError('Missing required parameter "progress"')

                timeline_source = episode_mapping.timeline['source']

                if not (timeline_source.start <= progress <= timeline_source.end):
                    continue

            return EpisodeMatch(episode_mapping.season, episode_mapping.number)

        raise NotImplementedError

    def titles(self, key):
        pass

    def __getitem__(self, key):
        pass
