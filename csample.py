"""
csample: Consistent sampling library for Python
"""
from __future__ import division
import xxhash


def main():
    pass


def sample_tuple(s, rate, col, funcname='xxhash32', salt='DEFAULT_SALT'):
    """Sample tuples in given stream `s`.

    Performs consistent sampling with given sampling `rate` by applying a hash
    function `funcname`. Sampling with the same `salt` (or seed) always yields
    result.

    :param s: stream of tuples
    :param rate: sampling rate
    :param col: index of column to be hashed
    :param funcname: name of hash function: <xxhash32>
    :param salt: salt or seed for hash function
    :return: sampled stream of tuples
    """
    func = _hash_with_salt(funcname, salt)
    return (l for l in s if func(l[col]) < rate)


def sample_line(s, rate, funcname='xxhash32', salt='DEFAULT_SALT'):
    """Sample strings in given stream `s`.

    The function expects strings instead of tuples, except for that the
    function does the exactly same thing with `sample_tuple()`.

    :param s: stream of strings
    :param rate: sampling rate
    :param funcname: name of hash function: <xxhash32>
    :param salt: salt of seed for hash function
    :return: sample stream of strings
    """
    func = _hash_with_salt(funcname, salt)
    return (l for l in s if func(l) < rate)


def _hash_with_salt(funcname, salt):
    if funcname == 'xxhash32':
        seed = xxhash.xxh32(salt).intdigest()
        return lambda x: xxhash.xxh32(x, seed=seed).intdigest() / 0xFFFFFFFF
    else:
        raise ValueError('Unknown function name: %s' % funcname)


if __name__ == '__main__':
    main()
