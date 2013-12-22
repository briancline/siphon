from paramiko import Transport, SFTPClient
from time import sleep


class RemoteFileManager(object):
    def __init__(self, host, user, password, port=22):
        self._host = host
        self._port = port
        self._user = user
        self._pass = password

    def connect(self):
        self._transport = Transport((self._host, self._port))
        self._transport.connect(username=self._user, password=self._pass)
        self._client = SFTPClient.from_transport(self._transport)

    def files(self, path=None):
        path = '' if path is None else path
        return self._client.listdir(path)

    def file_text(self, path):
        return self._client.open(path, 'r').readlines()

    def lock_wait(self, path, sleep_time=3):
        while True:
            try:
                self._client.open(path, 'r')
                print('Waiting for lock on sums file to be released...')
                sleep(sleep_time)
            except Exception:
                ## No lock file present on remote
                break

    def file_iter(self, path):
        try:
            self._client.stat(path)
        except IOError:
            with self._client.open(path, 'w') as remote_file:
                remote_file.close()

        for line in self._client.open(path, 'r'):
            yield line
