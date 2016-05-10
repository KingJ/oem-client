from argparse import ArgumentParser
from flask import Flask, abort, send_from_directory
import logging
import os

app = Flask(__name__)
log = logging.getLogger(__name__)
packages = {}


@app.route('/<package>/<version>/<database>/<collection>/index.<extension>')
def serve_index(package, version, database, collection, extension):
    # Find database
    if package not in packages:
        abort(404)

    path = os.path.join(packages[package], database, collection)

    # Ensure index exists
    filename = 'index.%s' % extension

    if not os.path.exists(os.path.join(path, filename)):
        abort(404)

    # Serve file
    mimetype = None

    if extension.endswith('json'):
        mimetype = 'application/json'

    return send_from_directory(path, filename, mimetype=mimetype)

@app.route('/<package>/<version>/<database>/<collection>/items/<key>.<extension>')
def serve_item(package, version, database, collection, key, extension):
    # Find database
    if package not in packages:
        abort(404)

    path = os.path.join(packages[package], database, collection, 'items')

    # Ensure index exists
    filename = '%s.%s' % (key, extension)

    if not os.path.exists(os.path.join(path, filename)):
        abort(404)

    # Serve file
    mimetype = None

    if extension.endswith('json'):
        mimetype = 'application/json'

    return send_from_directory(path, filename, mimetype=mimetype)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--package', action='append')

    args = parser.parse_args()

    for path in args.package:
        packages[os.path.basename(path)] = path

    # Run server
    app.run(debug=False)
