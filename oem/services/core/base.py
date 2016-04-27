from oem_core.models import Database, Format

import logging
import os
import sys

log = logging.getLogger(__name__)


class Service(object):
    __services__ = {}

    def __init__(self, client, source, target):
        self.client = client
        self.source = source
        self.target = target

        self.database = None
        self.collection = None

        self._database_path = None

    def load(self):
        raise NotImplementedError

    def find_database(self):
        if not self.client.use_database_packages:
            return None

        if self._database_path is not None:
            return self._database_path

        names = [
            'oem_%s_%s' % (self.source, self.target),
            'oem_%s_%s' % (self.target, self.source)
        ]

        for package_path in [os.curdir] + self.client.search_paths + sys.path:
            # Ignore invalid paths
            if package_path.endswith('.egg') or package_path.endswith('.zip'):
                continue

            if not os.path.exists(package_path):
                continue

            # List items in `package_path`
            try:
                items = os.listdir(package_path)
            except Exception, ex:
                log.debug('Unable to list directory %r - %s', package_path, ex, exc_info=True)
                continue

            # Try find matching name in directory `items`
            for name in names:
                if name in items:
                    # Found database installation location
                    self._database_path = os.path.join(package_path, name)
                    return self._database_path

        # Unable to find database installation
        log.info('Unable to find database installation for: %s -> %s, using online database instead', self.source, self.target)
        return None

    def find_format(self, collection_path=None):
        if collection_path is None:
            collection_path = os.path.join(self.find_database(), self.source)

        # Retrieve available index formats
        names = os.listdir(collection_path)
        available = []

        for filename in names:
            if not filename.startswith('index.'):
                continue

            path = os.path.join(collection_path, filename)
            name, ext = os.path.splitext(filename)

            # Check for "msgpack" support
            if ext == 'mpack':
                # TODO ensure "msgpack" is available
                pass

            # Retrieve file modified date
            modified_date = os.path.getmtime(path)

            # Store index in `available` list
            available.append((modified_date, path))

        if len(available) < 1:
            raise Exception('No supported index available in %r' % collection_path)

        # Sort `available` by modified date
        available.sort(key=lambda i: i[0])

        # Use most recently modified index
        _, path = available[-1]

        # Parse index format from `path`
        return Format.from_path(path)

    def load_database(self, path=None):
        if path is None:
            path = self.find_database()

        # Find collection format
        fmt = self.find_format()

        if fmt is None:
            return False

        # Load database
        self.database = Database.load(path, fmt, self.source, self.target)
        return True

    def load_collection(self):
        # Ensure database is loaded
        if not self.load_database():
            return False

        # Load collection
        self.collection = self.database.load_collection(self.source, self.target)
        return self.collection
