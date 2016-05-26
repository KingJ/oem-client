from setuptools import setup


setup(
    name="oem",
    version="1.0.0",
    author="Dean Gardiner",
    author_email="me@dgardiner.net",

    install_requires=[
        'oem-core>=1.0.0',
        'oem-framework>=1.0.0',

        'appdirs>=1.4.0',
        'requests>=2.10.0',
        'semantic_version>=2.5.0'
    ]
)
