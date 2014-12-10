"""
csample: Consistent sampling library for Python
"""
import xxhash


def main():
    print(sample('Hello'))


def sample(s):
    """
    Blahblah

    :param s: blah
    :return: blah
    """
    return xxhash.xxh32(s).intdigest()


if __name__ == '__main__':
    main()
