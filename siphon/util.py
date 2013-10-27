from ConfigParser import SafeConfigParser
from argparse import ArgumentParser, FileType


def load_config(fd):
    defaults = {'remote': {'hostname': 'localhost',
                           'port': 22,
                           'username': 'guest',
                           'password': 'guest',
                           'sumfile': 'md5sums.txt',
                           'lockfile': '.siphon.lock'},
                'db': {'filename': 'siphon.db'}}

    config = SafeConfigParser(defaults)
    config.readfp(fd)
    fd.close()

    return config


def load_parser():
    parser = ArgumentParser(
        description='Intelligently siphons files from a remote host')
    parser.add_argument('-f', '--config-file', type=FileType('r'),
                        default='config.ini',
                        help='Path to the Siphon config file')
    return parser
