#!/usr/bin/env python
from __future__ import print_function
from os.path import basename
#from pprint import pprint
from siphon.util import load_parser, load_config
from siphon.db import DBManager
from siphon.manager import RemoteFileManager

config = None


def main():
    db = DBManager(config.get('db', 'filename'))
    files = db.get_all_remote()
    print("Loaded %d files from local database." % len(files))

    remote = RemoteFileManager(config.get('remote', 'hostname'),
                               config.get('remote', 'username'),
                               config.get('remote', 'password'),
                               port=config.getint('remote', 'port'))
    remote.connect()
    remote.lock_wait(config.get('remote', 'lockfile'))

    new_count = 0
    for line in remote.file_iter(config.get('remote', 'sumfile')):
        if not line:
            continue

        ## Use None as the delimiter so the two spaces after hash that md5sum
        ## generates are treated as one delimiter
        bits = line.strip().split(None, 1)
        file_sum = bits[0]
        file_path = bits[1]

        record = db.get_sum(file_sum=file_sum)
        if not record:
            print('New remote file: %s => %s' % (file_sum, file_path))
            db.add_file(file_sum=file_sum,
                        file_name=basename(file_path),
                        path=file_path)
            new_count += 1

    print('Found %d new files in remote list.' % new_count)

    ## TODO: transfer down any new files


if __name__ == '__main__':
    parser = load_parser()
    args = parser.parse_args()

    config = load_config(args.config_file)
    main()
