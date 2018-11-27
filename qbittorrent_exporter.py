import argparse
import flask
import requests

app = flask.Flask(__name__)


class QBittorrentApi:
    def __init__(self, address):
        self._address = address
        self._session = requests.Session()
        super(QBittorrentApi, self).__init__()

    def _build_url(self, api_name, method_name):
        return 'http://{address}/api/v2/{api_name}/{method_name}'.format(
            address=self._address, api_name=api_name, method_name=method_name)

    def login(self, username, password):
        r = self._session.post(self._build_url('auth', 'login'), data={'username': username, 'password': password})
        r.raise_for_status()

    def peer_log(self):
        r = self._session.get(self._build_url('log', 'peers'))
        return r.json()

    def transfer_info(self):
        r = self._session.get(self._build_url('transfer', 'info'))
        return r.json()

    def torrents_info(self):
        r = self._session.get(self._build_url('torrents', 'info'))
        return r.json()

    def torrents_properties(self, torrent_hash):
        r = self._session.get(self._build_url('torrents', 'properties'), data={'hash': torrent_hash})
        return r.json()

    def torrents_trackers(self, torrent_hash):
        r = self._session.get(self._build_url('torrents', 'trackers'), data={'hash': torrent_hash})
        return r.json()


@app.route("/metrics")
def metrics():
    return "Hello World!"


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--address', default='localhost:8080', help='qBittorrent address to connect')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default='8885')
    parser.add_argument('--username', default='admin')
    parser.add_argument('--password', default='adminadmin')

    args = parser.parse_args()

    app.config.update(vars(args))

    app.config['api'] = QBittorrentApi(app.config['address'])
    app.config['api'].login(
        username=app.config['username'],
        password=app.config['password']
    )

    app.run(
        host=app.config['host'],
        port=app.config['port'],
    )


if __name__ == '__main__':
    main()
