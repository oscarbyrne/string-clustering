from argparse import ArgumentParser
from pprint import pprint

from stringclusters import (
    clustered,
    jaro_winkler_distance,
)


parser = ArgumentParser(
    description='''
    Cluster strings via K-Medoids method according to their Jaro-Winkler distance
    '''
)
parser.add_argument(
    '-i',
    metavar='iterations',
    dest='iterations',
    type=int,
    default=5,
    help='Maximum number of iterations (default: 5)'
)
parser.add_argument(
    '-c', '--cached',
    action='store_true',
    help='Use cached version of the algorithm'
)
parser.add_argument(
    'strings_file',
    help='Location of the file to read strings from'
)
parser.add_argument(
    'n_clusters',
    type=int,
    help='Number of clusters'
)


def do_clustering(strings_file, n_clusters, iterations):
    with open(strings_file) as f:
        strings = tuple(line.rstrip() for line in f)

    return clustered(strings, n_clusters, jaro_winkler_distance, iterations)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.cached:
        raise NotImplementedError()
    else:
        clusters = do_clustering(args.strings_file, args.n_clusters, args.iterations)

    pprint(clusters)

