#read in chunks


def read_in_chunks(file_object, chunk_size=1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.

    usage::
            f = open('really_big_file.dat')
            for piece in read_in_chunks(f):
                process_data(piece)

    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def get_files_by_suffix(dir, blacklist=None):
    pass


def get_immediate_files_by_suffix(dir, blacklist=None):
    pass

def get_blacklist_expressions(blacklist_file):
    pass


#
# SORTING
#

from operator import itemgetter, attrgetter

def sort_iterable_by_attr_names(iterable, attr_names, descending=False):
    """
    input:
          
          - list of objects:    [Dog('john', 'A', 15), Dog('jane', 'B', 12), Dog('dave', 'B', 10)]
          - list of dicts:      [{'key1': 'john', A': 15}, {'key1':'jane', 'B': 12}, {'key1':'dave', 'B': 10}]
          - tuple of dicts
          - tuple of objects
    return:
          - always a list of iterable

    usage ::
            sort_iterable_by_attr_names(iterable, ('age',))
            sort_iterable_by_attr_names(iterable, ('grade', 'age'))
            sort_iterable_by_attr_names(iterable, ('key1'))
    """
    return sorted(iterable, key=attrgetter(*attr_names), reverse=descending)



def sort_iterable_by_items_positions(iterable, items_positions, descending=False):
    """
    input:
          - list if tuples:     [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
          - list of lists:      [['john', 'A', 15], ['jane', 'B', 12], ['dave', 'B', 10]]
          - tuple of tuples
          - tuple of lists
    return:
          - always a list of iterable

    usage::
            sort_iterable_by_items_positions(iterable, (3,))
            sort_iterable_by_items_positions(iterable, (1,3,4))
            sort_iterable_by_items_positions(iterable, (1,3,4), True)
    """
    return sorted(iterable, key=itemgetter(*items_positions), reverse=descending)
