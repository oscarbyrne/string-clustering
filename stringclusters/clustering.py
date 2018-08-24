import random
from functools import partial


def clustered(items, n_clusters, distance, iterations):

    def associate(items, medoids):
        clusters = {medoid: [] for medoid in medoids}
        for o in items:
            medoid = min(
                medoids,
                key=lambda m: distance(m, o)
            )
            clusters[medoid].append(o)
        return clusters

    def calculate_medoid(items):
        return min(items, key=partial(total_distance, items))

    def cost(solution):
        return sum(
            total_distance(items, medoid) for medoid, items in solution.items()
        )

    def total_distance(items, medoid):
        return sum(distance(medoid, o) for o in items)

    previous = {}

    clusters = associate(
        items,
        random.sample(items, n_clusters)
    )

    # wait for solution to converge
    for i in range(iterations):
        previous = clusters
        clusters = associate(
            items,
            [calculate_medoid(cluster) for cluster in clusters.values()]
        )

        if cost(clusters) == cost(previous):
            break

    return clusters


if __name__ == '__main__':
    from metrics import jaro_winkler_distance
    test_data = {
        'hello',
        'hellx',
        'test',
        'tester',
        'nope',
        'nope2',
    }
    expected = {
        'hellx': ['hellx', 'hello'],
        'nope': ['nope', 'nope2'],
        'tester': ['tester', 'test']
    }
    assert clustered(test_data, 3, jaro_winkler_distance, 5) == expected
