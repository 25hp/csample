import xxhash


def main():
    print(sample('Hello'))


def sample(s):
    return xxhash.xxh32(s).intdigest()


if __name__ == '__main__':
    main()
