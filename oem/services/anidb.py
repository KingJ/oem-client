from oem.media.show.mapper import ShowMapper
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

    def map(self, key, identifier):
        # Retrieve item
        item = self.get(key)

        if item is None:
            return None

        # Map episode
        return self.mapper.match(item, identifier)

    def titles(self, key):
        pass

    def __getitem__(self, key):
        pass
