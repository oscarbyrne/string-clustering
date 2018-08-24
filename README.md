# string-clustering
Using k-medoids clustering to group strings via jaro winkler distance metric

## To run

  ```bash
  $ python3 sample.py -h
  
  usage: sample.py [-h] [-i iterations] [-c] strings_file n_clusters

  Cluster strings via K-Medoids method according to their Jaro-Winkler distance

  positional arguments:
    strings_file   Location of the file to read strings from
    n_clusters     Number of clusters

  optional arguments:
    -h, --help     show this help message and exit
    -i iterations  Maximum number of iterations (default: 5)
    -c, --cached   Use cached version of the algorithm
  ```

## Cached mode

To try and speed up the processing time I implemented a sqlite database to act as a lookup table
containing string pairs and their distances. You can access this experimental mode by passing
the `-c` flag. Note that, in its current version, this is actually slower than calculating the
Jaro Winkler distance on the fly! In future versions this can be significantly improved by
offloading certain calculations to the database from Python.

## TODO

1. Optimize the clustering algorithm in cached mode:
    - design an interface for collections of strings containing the abstract methods needed
      for k-medoid clustering (aka what are currently encapsulated by the functions `associate`,
      `calculate_medoid` etc). In my understanding this could be considered the 'Domain layer'
      and the generalized clustering function would be 'Application layer'
    - implement this interface for both an in-RAM version (aka use existing code) and
      a database version using SQLite commands
    - refactor entry point (`sample.py`) to pass the appropriate domain model into the
      clustering algorithm depending on the selected mode
