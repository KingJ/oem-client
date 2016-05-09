from oem.providers.release.core.base import ReleaseProvider

import logging
import requests
import urlparse

log = logging.getLogger(__name__)


class IncrementalReleaseProvider(ReleaseProvider):
    def fetch(self, source, target, key, metadata):
        # TODO use current version
        version = '1.0.0'

        # Update item
        if not self.update_item(source, target, version, key, metadata):
            return False

        return True

    def update_database(self, source, target):
        available = self.version_available(source, target)
        current = self.version_current(source, target)

        if available == current:
            # Already up to date
            # TODO check data integrity
            return True

        # Update index
        if not self.update_index(source, target, available):
            return False

        return True

    def update_index(self, source, target, version):
        if self.storage.has_index(source, target, version):
            return True
    
        # Fetch index
        response = self._fetch(source, target, version, 'index.%s' % self.format.__extension__)

        if response is None:
            return False
    
        # Update cache
        return self.storage.update_index(source, target, version, response)

    def update_item(self, source, target, version, key, metadata):
        if self.storage.has_item(source, target, version, key):
            return True
    
        # Fetch index
        response = self._fetch(source, target, version, '/'.join([
            'items',
            '%s.%s' % (key, self.format.__extension__)
        ]))
    
        # Update cache
        return self.storage.update_item(source, target, version, key, response, metadata)

    def version_available(self, source, target):
        # TODO Retrieve latest version available
        return '1.0.0'

    def version_current(self, source, target):
        # TODO Retrieve current version
        return None

    def _fetch(self, source, target, version, filename):
        # Build URL
        url = self._build_url(source, target, version, filename)

        if url is None:
            return None

        # Fetch file
        try:
            response = requests.get(url, stream=True)
        except requests.ConnectionError, ex:
            log.warn('Unable to fetch file %r - %s', filename, ex)
            return None

        if response.status_code != 200:
            return None

        return response

    def _build_url(self, source, target, version, path):
        if self.database_url is None:
            return None

        return urlparse.urljoin(
            self.database_url,
            '/'.join([
                self._client.package_name(source, target), version,
                self._client.database_name(source, target), source,
                path
            ])
        )
