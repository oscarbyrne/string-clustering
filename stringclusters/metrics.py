from os.path import commonprefix


def jaro_winkler_distance(a, b, p=0.1):
    j = jaro_similarity(a, b)
    l = len(
        commonprefix((a, b))
    )
    return 1 - (j + l * p * (1 - j))


def jaro_similarity(a, b):

    if not (a and b):
        return 0.0

    m1 = matching(a, b)
    m2 = matching(b, a)

    if not (m1 and m2):
        return 0.0

    transposed = tuple(
        c1 for c1, c2 in zip(m1, m2) if c1 != c2
    )

    return (
        len(m1) / len(a) +
        len(m2) / len(b) +
        (len(m1) - len(transposed) / 2) / len(m1)
    ) / 3


def matching(a, b):

    search_radius = max(
        0,
        max(len(a), len(b)) // 2 - 1
    )

    matching = []

    for i, char in enumerate(a):
        start = max(
            0,
            i - search_radius
        )
        stop = min(
            i + search_radius + 1,
            len(b)
        )
        window = b[start:stop]
        if char in window:
            matching.append(char)

    return tuple(matching)


if __name__ == '__main__':
    from math import isclose
    # Test examples from: https://rosettacode.org/wiki/Jaro_distance
    sig_figs = 10
    assert isclose(0.9444444444, jaro_similarity('MARTHA', 'MARHTA'),           abs_tol=10**-sig_figs) 
    assert isclose(0.7666666667, jaro_similarity('DIXON', 'DICKSONX'),          abs_tol=10**-sig_figs) 
    assert isclose(0.8962962963, jaro_similarity('JELLYFISH', 'SMELLYFISH'),    abs_tol=10**-sig_figs) 
