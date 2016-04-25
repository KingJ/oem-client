from oem import OemClient

import logging


def run():
    # Initialize client
    client = OemClient()
    client.load_all()

    result = client['anidb'].to('tvdb').map('3', 1, 2)
    print

    result = client['anidb'].to('tvdb').map('818', 0, 1)
    print

    # Movies
    movie_anidb_7103 = client['anidb'].to('imdb').get(7103)

    movie_imdb_tt1663145 = client['imdb'].to('anidb').get("tt1663145")

    # Shows
    show_anidb_3 = client['anidb'].to('tvdb').get(3)

    show_tvdb_70973 =  client['tvdb'].to('anidb').get( 70973)
    show_tvdb_71551 =  client['tvdb'].to('anidb').get( 71551)
    show_tvdb_103691 = client['tvdb'].to('anidb').get(103691)
    show_tvdb_136251 = client['tvdb'].to('anidb').get(136251)
    show_tvdb_137151 = client['tvdb'].to('anidb').get(137151)
    show_tvdb_138691 = client['tvdb'].to('anidb').get(138691)

    print


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()
