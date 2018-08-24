from os.path import isfile
from itertools import combinations
import sqlite3

from tqdm import tqdm


class DistanceCache():

    def compile(self):
        with open(self.src) as f:
            entries = tuple(
                line.rstrip() for line in f
            )
        pairs = combinations(entries, 2)
        conn = sqlite3.connect(self.db)
        curs = conn.cursor()
        curs.execute(
            '''
            CREATE TABLE distances
            (a text, b text, distance real)
            '''
        )
        n = len(entries)
        npairs = n*(n-1)//2
        for a, b in tqdm(pairs, total=npairs):
            a, b = sorted((a, b))
            d = self.distance(a, b)
            curs.execute(
                '''
                INSERT INTO distances VALUES
                (?, ?, ?)
                ''',
                (a, b, d)
            )
            conn.commit()

        conn.close()

    def __init__(self, src, distance):
        self.src = src
        self.distance = distance
        self.conn = None
        if isfile(self.db):
            pass
        else:
            self.compile()

    @property
    def db(self):
        return f'.cache__{self.src}'

    def get_distance(self, a, b):
        if a == b:
            return 0.0
        a, b = sorted((a, b))
        records = self.curs.execute(
            '''
            SELECT distance
            FROM distances
            WHERE a = ? AND b = ?
            ''',
            (a, b)
        ).fetchall()
        assert len(records) == 1
        return records[0][0]

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.curs = self.conn.cursor()
        return self.get_distance
        
    def __exit__(self, type, value, traceback):
        self.conn.close()
        self.conn = None
        self.curs = None
