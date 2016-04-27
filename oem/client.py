from oem.services import SERVICES


class Client(object):
    def __init__(self, search_paths=None, use_database_packages=True):
        """OpenEntityMap (OEM) Client

        :param use_database_packages: True  = Use installed database packages (if available),
                                      False = Ignore installed database packages
        :type use_database_packages: bool
        """

        self.search_paths = search_paths or []
        self.use_database_packages = use_database_packages

        # Construct services
        self.services = self._construct_services()  # { (<source>, <target>): <service> }

    def load_all(self):
        for service in self.services.itervalues():
            service.load()

    def __getitem__(self, source):
        return ServiceInterface(self, source)

    #
    # Private methods
    #

    def _construct_services(self):
        result = {}

        for key, cls in SERVICES.items():
            # Add supported service conversions
            for source, targets in cls.__services__.items():
                for target in targets:
                    # Construct service
                    result[(source, target)] = cls(self, source, target)

        return result


class ServiceInterface(object):
    def __init__(self, client, source):
        self.client = client
        self.source = source

    def to(self, target):
        try:
            return self.client.services[(self.source, target)]
        except KeyError:
            raise KeyError('Unknown service: %s -> %s' % (self.source, target))
